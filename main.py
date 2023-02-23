import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
kivy.require('1.9.1')

import platform

from functools import partial
from decimal import Decimal

import xlrd

Window.clearcolor = (0, 0.5, 0.5, 0)

workbook = xlrd.open_workbook("data.xls")

Builder.load_file('Neonatal_Prescribing.kv') #this makes it work on andoid. it also makes it go double-vision on windows

sheet = workbook.sheet_by_index(0)
global the_infusion_data
the_infusion_data = ['0', ' ', ' ', ' ', '0', '0', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1']
global the_concentration
the_concentration = [' ']
global need_to_update_concs
need_to_update_concs = [0]
global baby_weight
baby_weight = [0]
global default_sliders
default_sliders = [0, 0]
global doses
doses = [0,0]
global weight_has_altered
weight_has_altered = [0]
global text_colour_state
text_colour_state = [0]

class Controller(BoxLayout): #title text
    def __init__(self):
        super(Controller, self).__init__()

class Controller5(BoxLayout): #enter baby weight
    
    def __init__(self):
        super(Controller5, self).__init__()

    def enter_baby_weight(self, *args):

        #deletes any text which is not a numbet or a decimal point
        string_is_numeric = True
        string_length = len(self.babyweight.text)

        for index in range(string_length):

            acceptable_input = False
            for indexed in range(10):
                if self.babyweight.text[index] == str(indexed) or self.babyweight.text[index] == ".":
                    acceptable_input = True
            
            if acceptable_input == False:
                string_is_numeric = False
                
        if string_is_numeric == False:
            new_string = ""
            for index in range(string_length):

                acceptable_input = False
                for indexed in range(10):
                    if self.babyweight.text[index] == str(indexed) or self.babyweight.text[index] == ".":
                        acceptable_input = True
                
                if acceptable_input == True:
                    new_string = new_string + self.babyweight.text[index]
            self.babyweight.text = new_string

        if self.babyweight.text == "":
            baby_weight[0] = 0
        else:
            baby_weight[0] = float(self.babyweight.text)

            

        #resets everything if the weight is altered
        
        need_to_update_concs[0] = 1 
        the_concentration[0] = ' '
        weight_has_altered[0] = 1
        need_to_update_concs[0] = 1

        for index in range(23):
            the_infusion_data[index] = ' '

        the_infusion_data[0] = '0'
        the_infusion_data[4] = '0'
        the_infusion_data[5] = '0'
        default_sliders[0] = 1
        default_sliders[1] = 1

class Controller2(BoxLayout): #set lower rate

    def cb(self, *largs): #updates lower rate details
        self.lowrateadvise.text = "Minimum rate:"+'\n'+str(the_infusion_data[4])+'\n'+str(the_infusion_data[7])
        self.lowslide.min = float(the_infusion_data[4])
        self.lowslide.max = float(the_infusion_data[5])
        self.highrateadvise.text = "Maximum rate:"+'\n'+str(the_infusion_data[5])+'\n'+str(the_infusion_data[7])

        if self.lowrate.text == "":
            self.lowrate.text = "0"
            
        if float(self.lowrate.text) < float(the_infusion_data[4]) or float(self.lowrate.text) > float(the_infusion_data[5]): #force default if text entered out-of-range
            default_sliders[0] = 1
                    
        if default_sliders[0] == 0: #sets slider to follow input text, or defaults both to minimum on infusion change
            if self.lowslide.value < 0.9 * float(self.lowrate.text): #only adjusts slider if 10% difference to avoid self-alteration
                self.lowslide.value = float(self.lowrate.text)
            elif self.lowslide.value > 1.1 * float(self.lowrate.text):
                self.lowslide.value = float(self.lowrate.text)
        else:
            self.lowslide.value = float(the_infusion_data[4]) #default to minimum on infusion change
            self.lowrate.text = str(the_infusion_data[4])
            default_sliders[0] = 0

        doses[0] = float(self.lowrate.text)

        if the_infusion_data[6] != " " and the_infusion_data[6] != "":
            if doses[0] > float(the_infusion_data[6]):
                self.lowrate.background_color = (0.9, 0.5, 0, 1)
            else:
                self.lowrate.background_color = (1, 1, 1, 1)
        else:
            self.lowrate.background_color = (1, 1, 1, 1)
        
        pass



    def move_slider1(self, *args):
        self.lowrate.text = str(int(args[1]*float(the_infusion_data[23]))/float(the_infusion_data[23])) #sets low rate box from moving slider; the_unfusion_data[23] relates to the number of decimal places
        Clock.unschedule(self.cb)
        Clock.schedule_interval(self.cb, 0.1)
        pass

    def enter_low_rate(self, *args): #when text changes

        #deletes any text entered that is not numeric

        string_is_numeric = True
        string_length = len(self.lowrate.text)
        
        for index in range(string_length):

            acceptable_input = False
            for indexed in range(10):
                if self.lowrate.text[index] == str(indexed) or self.lowrate.text[index] == ".":
                    acceptable_input = True
            
            if acceptable_input == False:
                string_is_numeric = False
                
        if string_is_numeric == False:
            new_string = ""
            for index in range(string_length):

                acceptable_input = False
                for indexed in range(10):
                    if self.lowrate.text[index] == str(indexed) or self.lowrate.text[index] == ".":
                        acceptable_input = True
                
                if acceptable_input == True:
                    new_string = new_string + self.lowrate.text[index]
            self.lowrate.text = new_string

        Clock.unschedule(self.cb)
        Clock.schedule_interval(self.cb, 2) #causes 2 second delay in action to allow user to finish entering text
        pass

    def user_hit_return(self, *args):
        Clock.unschedule(self.cb)
        Clock.schedule_interval(self.cb, 0.1) #causes no delay in action if user hits enter key
        pass

    def __init__(self, **kwargs):
        self._trigger = Clock.create_trigger(self.cb)
        super(Controller2, self).__init__()
        self.bind(x=self._trigger, y=self._trigger)
        Clock.schedule_interval(self.cb, 0.1)

class Controller4(BoxLayout): #set upper rate

    def cb(self, *largs): #updates higher rate details at intervals
        self.lowrateadvise.text = "Minimum rate:"+'\n'+str(the_infusion_data[4])+'\n'+str(the_infusion_data[7])
        self.highslide.min = float(the_infusion_data[4])
        self.highslide.max = float(the_infusion_data[5])
        self.highrateadvise.text = "Maximum rate:"+'\n'+str(the_infusion_data[5])+'\n'+str(the_infusion_data[7])

        if self.highrate.text == "":
            self.highrate.text = "0"

        if float(self.highrate.text) < float(the_infusion_data[4]) or float(self.highrate.text) > float(the_infusion_data[5]): #force default if text entered out-of-range
            default_sliders[1] = 1
        
        if default_sliders[1] == 0: #sets slider to follow input text, or defaults both to minimum on infusion change
            if self.highslide.value < 0.9 * float(self.highrate.text): #only adjusts slider if 10% difference to avoid self-alteration
                self.highslide.value = float(self.highrate.text)
            elif self.highslide.value > 1.1 * float(self.highrate.text):
                self.highslide.value = float(self.highrate.text)
        else:
            self.highslide.value = float(the_infusion_data[4]) #default to minimum on infusion change
            self.highrate.text = str(the_infusion_data[4])
            default_sliders[1] = 0

        doses[1] = float(self.highrate.text)

        if the_infusion_data[6] != " " and the_infusion_data[6] != "":
            if doses[1] > float(the_infusion_data[6]):
                self.highrate.background_color = (0.9, 0.5, 0, 1)
            else:
                self.highrate.background_color = (1, 1, 1, 1)
        else:
            self.highrate.background_color = (1, 1, 1, 1)

        pass

    def move_slider2(self, *args):
        self.highrate.text = str(int(args[1]*float(the_infusion_data[23]))/float(the_infusion_data[23])) #sets low rate box from moving slider; the_unfusion_data[23] relates to the number of decimal places
        Clock.unschedule(self.cb)
        Clock.schedule_interval(self.cb, 0.1)
        pass

    def enter_high_rate(self, *args): #when text changes

        #deletes any text entered that is not numeric

        string_is_numeric = True
        string_length = len(self.highrate.text)
        
        for index in range(string_length):

            acceptable_input = False
            for indexed in range(10):
                if self.highrate.text[index] == str(indexed) or self.highrate.text[index] == ".":
                    acceptable_input = True
            
            if acceptable_input == False:
                string_is_numeric = False
                
        if string_is_numeric == False:
            new_string = ""
            for index in range(string_length):

                acceptable_input = False
                for indexed in range(10):
                    if self.highrate.text[index] == str(indexed) or self.highrate.text[index] == ".":
                        acceptable_input = True
                
                if acceptable_input == True:
                    new_string = new_string + self.highrate.text[index]
            self.highrate.text = new_string
        
        Clock.unschedule(self.cb)
        Clock.schedule_interval(self.cb, 2) #causes 2 second delay in action to allow user to finish entering text
        pass

    def user_hit_return(self, *args):
        Clock.unschedule(self.cb)
        Clock.schedule_interval(self.cb, 0.1) #causes no delay in action if user hits enter key
        pass

    def __init__(self, **kwargs):
        self._trigger = Clock.create_trigger(self.cb)
        super(Controller4, self).__init__()
        self.bind(x=self._trigger, y=self._trigger)
        Clock.schedule_interval(self.cb, 0.1)

class Controller3(BoxLayout):
    def __init__(self):
        super(Controller3, self).__init__()

class The_First_Dropdown(BoxLayout): #select infusion

    def cb(self, *largs): #updates concentration options
        if weight_has_altered[0] == 1:
            self.make_the_first_dropdown('yes')
            weight_has_altered[0] = 0
        pass
    
    def infusion_got_selected(self, args1, args2, args3): #args 3 will be the dropdown text
        
        for index in range(26): #tests to see which row was chosen

            if args3 == sheet.cell_value(index, 1):
                row_chosen = index

        if row_chosen > 0:
            for index in range(24):
                the_infusion_data[index] = sheet.cell_value(row_chosen, index) #asign cells as list items in the_unfusion_data
                
        need_to_update_concs[0] = 1
        default_sliders[0] = 1
        default_sliders[1] = 1
        the_concentration[0] = ' '
        
        return callable

    def make_the_first_dropdown(self, initiate):
        # select infusion
        dropdown = DropDown()
        infusionbutton = Button(text='Select infusion', height=35)
        for index in range(22):

            if baby_weight[0] >= 0.1 and baby_weight[0] <= 10: #ensure baby weight acceptable
                btn = Button(text=sheet.cell_value(index + 4, 1), size_hint_y=None) #adds the infusions from the spreadsheet to the dropdown
                btn.bind(on_release=lambda btn: dropdown.select(btn.text))
                dropdown.add_widget(btn)

        infusionbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=partial(self.infusion_got_selected, 'text')) 
        dropdown.bind(on_select=lambda instance, x: setattr(infusionbutton, 'text', x))

        if weight_has_altered[0] == 1:
            self.clear_widgets()
        self.add_widget(infusionbutton)

    def __init__(self, **kwargs):
        self._trigger = Clock.create_trigger(self.cb)
        super(The_First_Dropdown, self).__init__(*kwargs)
        self.bind(x=self._trigger, y=self._trigger)
        Clock.schedule_interval(self.cb, 0.1)
        self.make_the_first_dropdown('yes')
        

class The_Second_Dropdown(BoxLayout): #select concentration

    def cb(self, *largs): #updates concentration options
        if need_to_update_concs[0] == 1:
            self.make_the_second_dropdown('yes')
            need_to_update_concs[0] = 0
        pass

    def make_the_second_dropdown(self, re_initiate):

        available_weights = [0, 0, 0]
        recommended_strength = 0
        
        if float(baby_weight[0]) < 1: #assigns available infusion strengths to 'available weights'
            available_weights[0] = 12
            available_weights[1] = 13
            available_weights[2] = 14
            
        elif float(baby_weight[0]) >= 2.5:
            available_weights[0] = 18
            available_weights[1] = 19
            available_weights[2] = 20
        else:
            available_weights[0] = 15
            available_weights[1] = 16
            available_weights[2] = 17

        if sheet.cell_value(int(the_infusion_data[0]), available_weights[2]) != "": #figures out how many strengths are available
            total_weights_available = 3
        elif sheet.cell_value(int(the_infusion_data[0]), available_weights[1]) != "":
            total_weights_available = 2
        elif sheet.cell_value(int(the_infusion_data[0]), available_weights[0]) != "":
            total_weights_available = 1
        else:
            total_weights_available = 0

        #recommended strengths:

        # Weight		Cutoff between high and low concentration	
        # < 1Kg		        0.75 Kg	
        # 1 - 2.49 Kg		1.75 Kg	
        # 2.5 Kg +		3.5 Kg	

        # recommended_strength will be set at 0 to 2 depending on which of available_weights[] is recommended

        if float(baby_weight[0]) < 1:                 #determining recommended strength
            if float(baby_weight[0]) < 0.75:
                if total_weights_available == 2:
                    recommended_strength = 1
                else:
                    recommended_strength = 2
            else:
                if total_weights_available == 2:
                    recommended_strength = 2
                else:
                    recommended_strength = 3
        elif float(baby_weight[0]) >= 2.5:
            if float(baby_weight[0]) < 3.5:
                if total_weights_available == 2:
                    recommended_strength = 1
                else:
                    recommended_strength = 2
            else:
                if total_weights_available == 2:
                    recommended_strength = 2
                else:
                    recommended_strength = 3
        else:
            if float(baby_weight[0]) < 1.75:
                if total_weights_available == 2:
                    recommended_strength = 1
                else:
                    recommended_strength = 2
            else:
                if total_weights_available == 2:
                    recommended_strength = 2
                else:
                    recommended_strength = 3
        if total_weights_available == 1:
            recommended_strength = 1
                
        
        dropdown = DropDown()
        concbutton = Button(text='Select concentration', height=35, halign='center')
        for index in range(total_weights_available):

            this_strength_recommended = "" #inserting 'recommended' next to recommended strength
            if index == recommended_strength - 1:
                this_strength_recommended = " *"
            if total_weights_available == 1: #but not if there's only one strength available
                this_strength_recommended = ""

            volume_with_decimals = float(sheet.cell_value(int(the_infusion_data[0]), 8))
            volume_without_decimals = int(volume_with_decimals) #removes decimal places from the volume

            dose_with_decimals = float(sheet.cell_value(int(the_infusion_data[0]), available_weights[index])) #removes decimal places from the concentration
            decimal_multiplier = 1
            for indexed in range(int(sheet.cell_value(int(the_infusion_data[0]), 24))):
                decimal_multiplier = decimal_multiplier * 10
            dose_with_correct_decimals = (float(int(dose_with_decimals * decimal_multiplier)))/decimal_multiplier 
            
            if total_weights_available > 0: #prevents any dropdown appearing when an infusion not yet selected
                btn = Button(text=str(dose_with_correct_decimals)+" "+str(sheet.cell_value(int(the_infusion_data[0]), 11))+this_strength_recommended, size_hint_y=None) #adds possible concentrations to the dropdown                
                btn.bind(on_release=lambda btn: dropdown.select(btn.text+'\n'+'in '+str(volume_without_decimals)+' mL of '+str(sheet.cell_value(int(the_infusion_data[0]), 9))))
                dropdown.add_widget(btn)
            
        concbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=partial(self.concentration_got_selected, 'text')) 
        dropdown.bind(on_select=lambda instance, x: setattr(concbutton, 'text', x))

        if re_initiate == 'yes':
            self.clear_widgets()
        self.add_widget(concbutton)

    def __init__(self, **kwargs):
        self._trigger = Clock.create_trigger(self.cb)
        super(The_Second_Dropdown, self).__init__(*kwargs)
        self.make_the_second_dropdown('no')
        self.bind(x=self._trigger, y=self._trigger)
        Clock.schedule_interval(self.cb, 0.2)

    def concentration_got_selected(self, args1, args2, args3):
        the_concentration[0] = args3 #retrieves the selection from the concentration dropdown however it is full-length
        pass

class Controller6(BoxLayout): #Gives the rates for the infusions and some accompanying notes

    def cb(self, *largs): #updates bottom text at intervals

        if baby_weight[0] >= 0.1 and baby_weight[0] <= 10: #ensure baby weight acceptable
            if int(the_infusion_data[0]) > 0:
                if the_concentration[0] != ' ':


                    concentrationstring = the_concentration[0] #extracting the number from the longer string selected in the dropdown; 'actual_conc'
                    concentrationnumber = ['','','','','']

                    conc_button_len = len(concentrationstring)
                    if conc_button_len == "":
                        conc_button_len = 5
                    
                    for index in range(5):
                        number_or_decimal = False
                        for indexed in range(10):
                            if concentrationstring[index] == str(indexed) or concentrationstring[index] == ".":
                                number_or_decimal = True
                        if number_or_decimal == True:
                            concentrationnumber[index] = concentrationstring[index]
                    actual_conc = concentrationnumber[0]+concentrationnumber[1]+concentrationnumber[2]+concentrationnumber[3]+concentrationnumber[4]

                    lower_rate =  ((float(baby_weight[0]) * doses[0] * the_infusion_data[21] * the_infusion_data[8])/((float(actual_conc) * the_infusion_data[22])))
                    higher_rate = ((float(baby_weight[0]) * doses[1] * the_infusion_data[21] * the_infusion_data[8])/((float(actual_conc) * the_infusion_data[22])))

                    lower_string = str(lower_rate) #for some reason i cannot use the int function to get the number of dp that i want
                    higher_string = str(higher_rate)

                    lower_3sf = "" #reduces to 4 characters
                    if len(lower_string) > 3:
                        if lower_string[3] != ".":
                            lower_3sf = lower_string[0] + lower_string[1] + lower_string[2] + lower_string[3]
                        else:
                            lower_3sf = lower_string[0] + lower_string[1] + lower_string[2]
                    else:
                        lower_3sf = lower_string

                    higher_3sf = "" #reduces to 4 characters
                    if len(higher_string) > 3:
                        if higher_string[3] != ".":
                            higher_3sf = higher_string[0] + higher_string[1] + higher_string[2] + higher_string[3]
                        else:
                            higher_3sf = higher_string[0] + higher_string[1] + higher_string[2]   
                    else:
                        higher_3sf = higher_string

                    if lower_3sf != higher_3sf: #only says 'between' if the two rates are different
                        self.outputtext1.text = 'Prescribe '+the_infusion_data[1]+'\n'+'between '+lower_3sf+' and '+higher_3sf+' mL/hour'
                    else:
                        self.outputtext1.text = 'Prescribe '+the_infusion_data[1]+'\n'+'at '+lower_3sf+' mL/hour'
                    Window.clearcolor = (0, 0.15, 0, 0)
                    
                    if the_infusion_data[3] != '':
                        self.outputtext2.text = 'Administration route: '+the_infusion_data[2]+'. Note: '+the_infusion_data[3]
                    else:
                        self.outputtext2.text = 'Administration route: '+the_infusion_data[2]
                else:
                    self.outputtext1.text = 'Set rates and select a concentration'
                    Window.clearcolor = (0, 0, 0.15, 0)

                    if the_infusion_data[3] != '':
                        self.outputtext2.text = 'Administration route: '+the_infusion_data[2]+'. Note: '+the_infusion_data[3]
                    else:
                        self.outputtext2.text = 'Administration route: '+the_infusion_data[2]

            else:
                self.outputtext1.text = 'Select an infusion'
                self.outputtext2.text = ''
                Window.clearcolor = (0.15, 0, 0.15, 0)
        else:
            self.outputtext1.text = 'Enter a weight between 0.1 and 10 Kg'
            self.outputtext2.text = 'Swipe up/down for Help/About'
            Window.clearcolor = (0.2, 0, 0, 0)

        if text_colour_state[0] == 0: #emphasize status with colour shimmer
            self.outputtext1.color = (1, 1, 1, 1) #(0.3, 0.8, 0.3, 1)
            text_colour_state[0] = 1
        else:
            self.outputtext1.color = (0.8, 0.8, 0.8, 0.8) #(0.3, 1, 0.3, 1)
            text_colour_state[0] = 0

        pass

    def __init__(self, **kwargs):
        self._trigger = Clock.create_trigger(self.cb)
        super(Controller6, self).__init__()
        self.bind(x=self._trigger, y=self._trigger)
        Clock.schedule_interval(self.cb, 0.2)

class Controller7(BoxLayout): #info screen
    def __init__(self):
        super(Controller7, self).__init__()
     
#main screen layout knitting together
layout = BoxLayout(orientation='vertical', spacing=20)
layout.add_widget(Controller())
layout.add_widget(Controller5())
layout.add_widget(The_First_Dropdown())
layout.add_widget(Controller2())
layout.add_widget(Controller4())
layout.add_widget(The_Second_Dropdown())
layout.add_widget(Controller6())

carousel = Carousel(direction='top', ignore_perpendicular_swipes = True, loop=True)

carousel.add_widget(layout) 
carousel.add_widget(Controller7()) #the 'about' screen


class Neonatal_PrescribingApp(App):

    def build(self):
        return carousel

if __name__ == '__main__':
    Neonatal_PrescribingApp().run()


