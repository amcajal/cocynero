################################################################################
#   Project: Cocynero
#
#   File: RecipeProcessor.py
#
#   Description:
#       Implements the "RecipeProcessor" class. This class provides a "template"
#   to perform the so called Extract-Transform-Load (ETL) process. The goal
#   of the class is (or at least try) to, once configured, generate a CSV
#   file called "recipes.csv", containing a list of recipes with their
#   required ingredientes.
#   The class needs 4 objects as parameters: @TODO explain this better
#
#   A common usage of this class will be the following:
#       '''
#       feeder = (...)
#       extract = (...)
#       transform = (...)
#       load = (...)
#       recipp = RecipeProcessor(feeder, extract, transform, load)
#       recipp.config()
#       recipp.run()
#       
#       '''
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

import sys

class RecipeProcessor():

    ############################################################################
    # ATTRIBUTES
    ############################################################################
    # This string is to be able to differentiate the error code lines from any other text line
    unique_error_tag = "COCYNERO_ERRCODE_"

    ############################################################################
    # METHODS
    ############################################################################

    def __init__(self,
                 feeder_obj=None,
                 extract_obj=None,
                 transform_obj=None,
                 load_obj=None):
        
        self.feeder_obj = feeder_obj
        self.extract_obj = extract_obj
        self.transform_obj = transform_obj
        self.load_obj = load_obj

        self.is_all_ready = False


    def cleanup(self):
        print("{class_name}: Cleanup method called. Cleaning Feeder-ETL resources...".format(class_name=self.__class__))
        self.feeder_obj.cleanup()
        self.extract_obj.cleanup()
        self.transform_obj.cleanup()
        self.load_obj.cleanup()
        self.is_all_ready = False
        

    def just_exit(self):
        print("{class_name}: Now exiting".format(class_name=self.__class__))
        sys.exit(0)

        
    def cleanup_and_exit(self):
        print("{class_name}: Cleanup and exit ...".format(class_name=self.__class__))
        self.cleanup()

        self.feeder_obj = None
        self.extract_obj = None
        self.transform_obj = None
        self.load_obj = None

        self.just_exit()
        
    
    def handle_error(self, error_code, **kwargs):
        error_title = "{class_name}: {tag}{ec}:".format(
            class_name=self.__class__,
            tag=self.unique_error_tag,
            ec=str(error_code))
        
        if (error_code==1):
            message=\
                 error_title + "Object {obj} could not be configured. ABORTING EXECUTION".format(obj=kwargs)
            do_this_action = self.cleanup_and_exit
            
        elif (error_code == 2):
            message=\
                error_title + "Some of the objects (Feeder, Extract, Transform, Load) failed the validation process. ABORTING EXECUTION."
            do_this_action = self.just_exit

        elif (error_code == 3):
            message=\
                error_title + "The following object is None: {obj_data}".format(obj_data=kwargs)
            do_this_action = None

        elif (error_code == 4):
            message=\
                error_title + "The object {obj_data} does NOT implement all required methods.".format(obj_data=kwargs)
            do_this_action = None

        elif (error_code == 5):
            message=\
                error_title + "The <object> does NOT implement <method:> {obj_method_data}".format(obj_method_data=kwargs)
            do_this_action = None

        elif (error_code == 6):
            message=\
                error_title + "Configuration of the RecipeProcessor object has FAILED. Cannot run yet."
            do_this_action = None

        elif (error_code == 7):
            message=\
                error_title + "The <data> generated by <method> is None: {data}. Ignoring this iteration".format(data=kwargs)
            do_this_action = None
            
        else:
            message="{class_name}: Unknown/uncontrolled error. This may be a bug.\n{details}".format(
                class_name = self.__class__,
                details=kwargs)
            do_this_action = self.cleanup_and_exit

        message_header = "\n"*3 + "*"*80 + "\n"
        message_footer = "\n" + "*"*80 + "\n"*3
        print("{header}{text}{footer}".format(header=message_header, text=message, footer=message_footer))
        
        if do_this_action:
            do_this_action()


    def generate_log_first_line(self):
        feeder_obj_name = "\tFeeder: " + type(self.feeder_obj).__name__ + "\n"
        extract_obj_name = "\tExtract: " + type(self.extract_obj).__name__ + "\n"
        transform_obj_name = "\tTransform: " + type(self.transform_obj).__name__ + "\n"
        load_obj_name = "\tLoad: " + type(self.load_obj).__name__ + "\n"

        separator_line = "*"*80 + "\n"
        obj_names = feeder_obj_name + extract_obj_name + transform_obj_name + load_obj_name
        first_line = "\n{sep}{title}{data}{sep}".format(sep=separator_line, title="FEEDER-ETL CONFIGURATION\n", data=obj_names)
        return first_line


    def check_for_required_methods(self, object_to_check):
        print("{class_name}: Checking that {obj} object implements the required methods..."\
              .format(class_name=self.__class__, obj=object_to_check.__class__))
        
        all_methods_defined = True
        
        # All objects must implement the following functions:
        # config(), cleanup(), cleanup_and_exit() and run()
        
        method = getattr(object_to_check, "config", None)
        if (not callable(method)):
            self.handle_error(error_code=5, obj=type(object_to_check), method="config method")
            all_methods_defined = False

        method = getattr(object_to_check, "cleanup", None)
        if (not callable(method)):
            self.handle_error(error_code=5, obj=type(object_to_check), method="cleanup method")
            all_methods_defined = False

        method = getattr(object_to_check, "run", None)
        if (not callable(method)):
            self.handle_error(error_code=5, obj=type(object_to_check), method="run method")
            all_methods_defined = False

        return all_methods_defined
    

    def validate_objects(self):
        print("{class_name}: Validating Feeder-ETL objects...".format(class_name=self.__class__))
        are_objects_ok = True
        
        # Check that no one of the objects (Feeder, Extract, Transform, Load) is None
        if (self.feeder_obj == None):
            self.handle_error(error_code=3, obj="feeder_obj")
            are_objects_ok = False
            
        if (self.extract_obj == None):
            self.handle_error(error_code=3, obj="extract_obj")
            are_objects_ok = False
            
        if (self.transform_obj == None):
            self.handle_error(error_code=3, obj="transform_obj")
            are_objects_ok = False
            
        if (self.load_obj == None):
            self.handle_error(error_code=3, obj="load_obj")
            are_objects_ok = False

        # Then, check each object define the required methods
        are_all_methods_defined = self.check_for_required_methods(self.feeder_obj)
        if (are_all_methods_defined == False):
            self.handle_error(error_code=4, obj_failing = type(self.feeder_obj))
            are_objects_ok = False

        are_all_methods_defined = self.check_for_required_methods(self.extract_obj)
        if (are_all_methods_defined == False):
            self.handle_error(error_code=4, obj_failing = type(self.extract_obj))
            are_objects_ok = False

        are_all_methods_defined = self.check_for_required_methods(self.transform_obj)
        if (are_all_methods_defined == False):
            self.handle_error(error_code=4, obj_failing = type(self.transform_obj))
            are_objects_ok = False

        are_all_methods_defined = self.check_for_required_methods(self.load_obj)
        if (are_all_methods_defined == False):
            self.handle_error(error_code=4, obj_failing = type(self.load_obj))
            are_objects_ok = False
            
        return are_objects_ok
            
        
    # Configure method
    def config(self):
        self.is_all_ready = True
        
        print(self.generate_log_first_line())

        # Check feeder, extraction, transform and load objets are NOT null
        # and that all of them define the required methods
        are_object_ok = self.validate_objects()
        if (are_object_ok == False):
            self.is_all_ready = False
            self.handle_error(error_code=2)

        print("{class_name}: Object validation is OK. Continue...".format(class_name=self.__class__))

        # Now, try to configure all objects
        print("{class_name}: Now configuring all Feeder-ETL objects...".format(class_name=self.__class__))
        
        is_config_ok = self.feeder_obj.config()
        if (is_config_ok == False):
            self.is_all_ready = False
            self.handle_error(error_code=1, obj_class=type(self.feeder_obj))
            
        is_config_ok = self.extract_obj.config()
        if (is_config_ok == False):
            self.is_all_ready = False
            self.handle_error(error_code=1, obj_class=type(self.extract_obj))
            
        is_config_ok = self.transform_obj.config()
        if (is_config_ok == False):
            self.is_all_ready = False
            self.handle_error(error_code=1, obj_class=type(self.transform_obj))
            
        is_config_ok = self.load_obj.config()
        if (is_config_ok == False):
            self.is_all_ready = False
            self.handle_error(error_code=1, obj_class=type(self.load_obj))

        # If process reachs this point, configuration has been successfull.
        print("{class_name}: Configuration successfull. \"run\" method can be executed.".format(class_name=self.__class__))
        
    def run(self):
        try:
            if (self.is_all_ready == False):
                self.handle_error(error_code=6)
                return
        
            # Start to process the data
            print("{class_name}: Starting \"run\" method: starting data processing operations...".format(class_name=self.__class__))
            while True:
                feeder_data = self.feeder_obj.run()
                if (feeder_data == None):
                    break
                
                extract_data = self.extract_obj.run(feeder_data)
                if (extract_data == None):
                    self.handle_error(error_code = 7, data="extract_data", method="extract_obj.run()")
                    continue
                
                transform_data = self.transform_obj.run(extract_data)
                if (transform_data == None):
                    self.handle_error(error_code = 7, data="transform_data", method="transform_obj.run()")
                    continue

                load_data = self.load_obj.run(transform_data)
                if (load_data == None):
                    self.handle_error(error_code = 7, data="load_data", method="load_obj.run()")
                    continue

            print("{class_name}: \"run\" method finished.".format(class_name=self.__class__))
            
        except Exception as e:
            # If code reaches here, at least try to provide as much
            # information as possible
            self.handle_error(error_code=999, cause=e)
            
        # Clean the data and exit
        self.cleanup()
