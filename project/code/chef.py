################################################################################
#   Project: Cocynero
#
#   File: chef.py
#
#   Description:
#       Implements the Chef class.
#
#       Chef class provides the core functionality of Cocynero project.
#       It reads data from the "recipes.csv" and "ingredients.csv", and
#       using such data, it is able to do thins like:
#       - Generate a weekly menu by randomly choose recipes (default 14)
#       - Generate the shooping list of the previous menu, listing all
#           required ingredients
#       - Search for recipes following several criterias (like "recipes
#           with 'eggs' word in its title")
#       and others.
#
#       Chef class should be the interface (or gateway) between the user
#       and the datasets (recipes.csv and ingredients.csv), so its design
#       must be focused in being easy to use and as intuitive as possible.
#
#   Notes: N/A
#
#   Contact: Alberto Martin Cajal, amartin.glimpse23<AT>gmail.com
#
#   URL: https://github.com/amcajal/cocynero
#
#   License: GNU GPL v3.0
#
#   Copyright (C) 2020 Alberto Martin Cajal
#
#   This file is part of Cocynero.
#
#   Cocynero is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Cocynero is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

import random

class Chef():

    ############################################################################
    # ATTRIBUTES
    ############################################################################

    # This values may change in the future and be establish in a separate module.
    # This values shall be used to acess the recipes data ONCE IT HAS BEEN
    # PROCESSED in the related data structure.
    field_separator = ";"
    title_field_index = 0
    url_field_index = 1
    ingr_field_index = 2 # "ingr" stands for "ingredients"
    not_apply_value = "n-a"


    ############################################################################
    # METHODS
    ############################################################################

    def __init__(self,
                 recipes_file="./recipes.csv",
                 shopping_list_file="./shopping_list.txt",
                 notes_file="./cocynero_notes.txt"):

        # By default, the input file with the recpes data is "recipes.csv"
        self.recipes_file_abspath = recipes_file

        # By default, the file where the shopping list will be written
        # is called "shopping_list.txt"
        self.shopping_list_file_abspath = shopping_list_file

        # When executing "tell_me_about" method (and probably others),
        # the result may be too big to handle or even read it properly in
        # a terminal, so the result is going to be written in this file too.
        self.notes_file_abspath = notes_file

        # This variable holds the configuration status of the chef object.
        # If false, several operations will be disabled until the object
        # is configured (moment in which the variable will be set to True)
        self.is_chef_configured = False

        # Dictionary holding ALL the recipes extracted from the recipes_file
        # It could be called "recipes_dict", but "book" represents
        # its intention in a better way.
        self.recipe_book = {}

        # List holding the recipes unique ids, selected after method "DoMenu" is run
        # The recipes are selected from the recipes_list, and the unique ids
        # are used to access to the recipe_book
        self.menu = []

        # List holding the ingredients of the recipes in "menu" dictionary
        self.shopping_list = []


    def cleanup(self):
        self.is_chef_configured = False
        self.recipe_book.clear()
        self.menu = []
        self.shopping_list = []


    def handle_error(self, error_code, **kwargs):
        # This is not a very user-friendly way to print errors.
        # Maybe this needs to be changed in the future.
        error_title = "{class_name}: ERROR CODE {ec}:".format(
            class_name=self.__class__,
            ec=str(error_code))

        if error_code == 1:
            message = \
                 error_title + "Chef could NOT be configured"
            do_this_action = None

        elif error_code == 2:
            message = \
                error_title + "Error with file {file}. Error is as follows: {e}\n".format(
                    file=self.recipes_file_abspath,
                    e=kwargs)
            do_this_action = None

        elif error_code == 3:
            message = \
                error_title + "The list of recipes is empty." \
                    + " Maybe the recipes file {f} is empty. Could NOT generate a menu".format(
                        f=self.recipes_file_abspath)
            do_this_action = None

        elif error_code == 4:
            message = error_title + "Bad unique ID (no recipe with such ID)." \
                + "\n\tBad ID is: {id}".format(id=kwargs)
            do_this_action = None


        message_header = "\n"*3 + "*"*80 + "\n"
        message_footer = "\n" + "*"*80 + "\n"*3
        print("{header}{text}{footer}".format(
            header=message_header,
            text=message,
            footer=message_footer))

        if do_this_action:
            do_this_action()


    # "Config" term represents with high accuracy what the function does,
    # but it is less friendly with non-technical users. "Get ready" is
    # quite the opposite: it really fits with the other functions
    # (i.e: "Chef, get ready, do menu, do shoppng list") but it is somehow
    # ambiguous.
    def config(self):
        self.is_chef_configured = False

        # Configuration involves:
        # - Checking if recipes_file exist and is readable
        # - Loading the contents of recipes_file into recipe_book
        # - Check the recipe_book is not empty
        try:
            print("Chef is reading recipes from {f}".format(f=self.recipes_file_abspath))
            with open(self.recipes_file_abspath, mode='r', encoding='utf-8') as reader:
                content = reader.readlines()

                # Lines starting with a # character are comments
                # so they are ignored
                valid_lines = list(filter(lambda x: not x.strip().startswith("#"), content))

                # Remove blank lines (Probably there is a better way to do this)
                valid_lines = [x for x in valid_lines if x]

                # Remove white-space characters (in a way that may be considered "overkill")
                valid_lines = [x.rstrip().strip().lstrip() for x in valid_lines if x]

                # Populate the dictionary
                # - Keys of the dictionary are Strings, representing unsigned integer numbers
                #   (the unique id value)
                # - Values of the dictionary are Lists, containing the recipe name, ingredients, etc
                for line in valid_lines:
                    fields = line.split(self.field_separator)

                    # When splitting the line by the field_separator,
                    # the index 0 element will be unique id value,
                    # while the rest of elements are the recipe title,
                    # the ingredients, etc
                    self.recipe_book[fields[0]] = fields[1:]


        except IOError as err:
            self.handle_error(error_code=2, error_details=err)
            return

        if not self.recipe_book:
            self.handle_error(error_code=3)
            return

        # Reaching here means configuration is done

        # Writing to this files may fail later, but at least, warn the user
        # about the intention of the program
        print("Chef will:\n-write shopping list in {f1}\n-write any other notes in {f2}".format(
            f1=self.shopping_list_file_abspath,
            f2=self.notes_file_abspath))
        print("Chef ready!")
        self.is_chef_configured = True


    # This is a rather simple function to "pretty print" a pair of
    # key-value from a dictionary, in a specific format that may be easily
    # changed in the future.
    # Because the "recipes_book" dictionary is the "single source of truth"
    # of the Chef class, only the key is required as input parameter
    def print_key_value(self, key):
        return "{k}: {v}".format(
            k=key,
            v=self.recipe_book[key][self.title_field_index])


    def show_menu(self):
        content_as_list = [self.print_key_value(k) for k in self.menu]
        content_as_text = "\n".join(content_as_list)
        print(content_as_text)
        try:
            print("Menu written also in {f}".format(f=self.notes_file_abspath))
            with open(self.notes_file_abspath, mode='w', encoding='utf-8') as writer:
                writer.write(content_as_text)
        except IOError as err:
            # Instead of using error_code = 2, maybe its a good idea to define
            # a different error code, specific for this situation
            self.handle_error(error_code=2, error_details=err)


    def print_shopping_list(self):
        shopping_list = "\n".join(self.shopping_list)
        print(shopping_list)
        try:
            with open(self.shopping_list_file_abspath, mode='w', encoding='utf-8') as writer:
                writer.write(shopping_list)
        except IOError as err:
            # Instead of using error_code = 2, maybe its a good idea to define
            # a different error code, specific for this situation
            self.handle_error(error_code=2, error_details=err)


    def do_shopping_list(self, recipes_list=None):
        # If the user inputs a list of unique IDs, the shopping list
        # is forcefully generated
        if recipes_list:
            self.shopping_list = []
            self.menu = [str(x) for x in recipes_list]

        # print_shopping_list could be called directly,
        # but "do_shopping_list" seems a more natural way
        # to ask for the shopping list (it avoids use the word "print")
        if not self.shopping_list:
            for unique_id in self.menu:
                try:
                    recipe_title = self.recipe_book[unique_id][self.title_field_index]
                except:
                    self.handle_error(error_code=4, bad_id=unique_id)
                    continue

                recipe_title_line = "### {id}: {title} ###".format(
                    id=unique_id,
                    title=recipe_title)

                ingredients = self.recipe_book[unique_id][self.ingr_field_index:]

                self.shopping_list.append(recipe_title_line)
                self.shopping_list = self.shopping_list + ingredients

        self.print_shopping_list()


    def do_menu(self, number_of_recipes=14):
        # If not configured, do first, and if fails, warn user
        # and exit method.
        # This may seem unefficient, but goal is to give the user
        # the opportunity to fix whatever problems lead to an incorrect
        # configuration.
        if not self.is_chef_configured:
            self.config()
            if not self.is_chef_configured:
                self.handle_error(error_code=1)
                return

        # Reaching here means config has been successfull
        # Now: generate the menu

        # Basic case, 10 unique keys from the dictionary, without repetition
        # random.sample() ensures no repetition elements
        self.menu = random.sample(list(self.recipe_book), number_of_recipes)

        # Shopping list is cleaned here, because its data only change
        # when a new menu is generated
        self.shopping_list = []

        # Finally, print the menu in the selected mode
        self.show_menu()


    # Append to the "menu" list all recipes with the specified "pattern"
    # in the specified "field" (i.e: all recipes with word "eggs" in "title")
    def find_matching_recipes(self, field, pattern):
        for unique_id in self.recipe_book:
            # This try-catch block should NOT be necessary, but it is leave
            # just for security (in case the recipes file is ill-formed or something)
            try:
                target_field = self.recipe_book[unique_id][field].lower()
            except:
                return

            if pattern in target_field:
                self.menu.append(unique_id)


    # Append to the "menu" list all recipes that use ANY
    # of the ingredients provided as input parameter
    # (i.e: input parameter is [eggs, olive oil], so find
    # all recipes using egss, olive oil, or both)
    def find_matching_ingredients(self, matching_ingredients, mode):
        for unique_id in self.recipe_book:
            # This try-catch block should NOT be necessary, but it is leave
            # just for security (in case the recipes file is ill-formed or something)
            try:
                recipe_ingredients = self.recipe_book[unique_id][self.ingr_field_index:]
            except:
                return

            # Turn all strings to lower(), so matching is easier (to avoid
            # the typical case where "eggs" are not found, but there are Eggs,
            # or even eGGS
            recipe_ingredients = [x.lower() for x in recipe_ingredients]
            matching_ingredients = [x.lower() for x in matching_ingredients]

            # Turn the recipe ingredients list in a single string, so the "any"
            # and "all" functions will work as intended. The goal is to find
            # if the strings in "matching_ingredients" are substrings of
            # the "recipe_ingredients". If this is done with lists, several
            # matches wont appear as such.
            # I.e: if matching_ingredients is ["eggs", "bacon"]
            # and recipe_ingredients is ["small eggs, "smoky bacon"], the following
            # call to "any" will return FALSE, because matching between lists only
            # works when the element X of a list is EXACTLY equal to element Y in the other list
            #
            #   any(x in recipe_ingredients for x in matching_ingredients)
            #
            # (this return false because element "eggs" is not found in recipe_ingredients)
            # Thats the root cause: comparision between elements instead of substring in string

            ingredients_string = ";".join(recipe_ingredients)

            if mode == "Some":
                method = any
            else:
                method = all

            if method(x in ingredients_string for x in matching_ingredients):
                self.menu.append(unique_id)


    # This function must be read as follows:
    # "Tell me about recipes ..."
    # - whose recipe id is <recipe_id>
    # - containing a title with this text pattern
    # - comming from an URL with this text pattern
    # - containing some or all of this ingredients
    #   (depending on the matching mode)
    def tell_me_about(self,
                      recipe_id=None,
                      title_with=None,
                      url_with=None,
                      ingredients=None,
                      matching_mode="Some"):

        #@TODO use a diferent list to store the matching recipes unique_ids?
        self.menu = []

        if recipe_id:
            # This is a dummy way to print a recipe data, but in the future
            # this could be enhanced
            try:
                print(self.recipe_book[str(recipe_id)])
            except:
                self.handle_error(error_code=4, bad_id=recipe_id)
            return

        elif title_with:
            pattern = title_with.lower()
            field = self.title_field_index

        elif url_with:
            pattern = url_with.lower()
            field = self.url_field_index

        elif ingredients:
            self.find_matching_ingredients(ingredients, matching_mode)
            self.show_menu()
            return

        self.find_matching_recipes(field, pattern)
        self.show_menu()
