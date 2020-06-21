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

from os import path
import random
import re

class Chef():

    ############################################################################
    # ATTRIBUTES
    ############################################################################

    # This values may change in the future and be establish in a separate module.
    # This values shall be used to acess the recipes data ONCE IT HAS BEEN
    # PROCESSED in the related data structure.
    field_separator=";"
    title_field_index= 0
    url_field_index= 1
    ingr_field_index=2 # "ingr" stands for "ingredients"  
    

    ############################################################################
    # METHODS
    ############################################################################
    
    def __init__(self,
                 recipes_file= "./recipes.csv",
                 shopping_list_file= "./shopping_list.txt"):
        
        # By default, the input file with the recpes data is "recipes.csv"
        self.recipes_file_abspath = recipes_file

        # By default, the file where the shopping list will be written
        # is called "shopping_list.txt"
        self.shopping_list_file_abspath = shopping_list_file

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
        
        if (error_code==1):
            message=\
                 error_title + "Chef could NOT be configured"
            do_this_action = None

        elif (error_code==2):
            message=\
                error_title + "Error with file {file}. Error is as follows: {e}\n".format(
                    file = self.recipes_file_abspath,
                    e = kwargs)
            do_this_action = None

        elif (error_code==3):
            message=\
                error_title + "The list of recipes is empty. Maybe the recipes file {f} is empty. Could NOT generate a menu".format(
                    f = self.recipes_file_abspath)
            do_this_action = None

        elif (error_code==4):
            message= error_title + "Bad unique ID (no recipe with such ID).\n\tBad ID is: {id}".format(id=kwargs)
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
            with open(self.recipes_file_abspath, mode='r', encoding='utf-8') as reader:
                content = reader.readlines()

                # Lines starting with a # character are comments
                # so they are ignored
                valid_lines = list(filter(lambda x: not x.strip().startswith("#"), content))

                # Remove blank lines (Probably there is a better way to do this)
                valid_lines = [x for x in valid_lines if x]

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

        if (not self.recipe_book):
            self.handle_error(error_code=3)
            return

        # Reaching here means configuration is done
        print("Chef ready!")
        self.is_chef_configured = True


    def show_menu(self):
        # Print only recipe ID and recipe title        
        for unique_id in self.menu:
            recipe_title = self.recipe_book[unique_id][self.title_field_index]
            print("{key}: {value}\n".format(
                key=unique_id,
                value = recipe_title))

                
    def print_shopping_list(self):
        shopping_list="\n".join(self.shopping_list)
        print(shopping_list)
        try:
            with open(self.shopping_list_file_abspath, mode='w', encoding='utf-8') as writer:
                writer.write(shopping_list)
        except IOerror as err:
            # Instead of using error_code=2, maybe its a good idea to define
            # a different error code, specific for this situation
            self.handle_error(error_code=2, error_details=err)

        
    def do_shopping_list(self, recipes_list=None):
        # If the user inputs a list of unique IDs, the shopping list
        # is forcefully generated
        if (recipes_list):
            self.shopping_list = []
            self.menu = [str(x) for x in recipes_list]
            
        # print_shopping_list could be called directly,
        # but "do_shopping_list" seems a more natural way
        # to ask for the shopping list (it avoids use the word "print")
        if (not self.shopping_list):
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
        
            
    def do_menu(self, number_of_recipes=10):
        # If not configured, do first, and if fails, warn user
        # and exit method.
        # This may seem unefficient, but goal is to give the user
        # the opportunity to fix whatever problems lead to an incorrect
        # configuration.
        if (self.is_chef_configured == False):
            self.config()
            if (self.is_chef_configured == False):
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
        # @TODO instead of reuse menu list, use a different list
        self.menu = []

        if(title_with):
            # The following assign is just to make code more readable
            pattern=title_with.lower()
            for unique_id in self.recipe_book:
                # This try-catch block should NOT be necessary, but it is leave
                # just for security (in case the recipes file is ill-formed or something)
                try:
                    recipe_title = self.recipe_book[unique_id][self.title_field_index].lower()
                except:
                    continue
                
                if (pattern in recipe_title):
                    self.menu.append(unique_id)

            self.show_menu()
        #https://stackoverflow.com/questions/740287/how-to-check-if-one-of-the-following-items-is-in-a-list
