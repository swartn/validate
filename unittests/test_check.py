import pytest
import validate.check as ch

plot = {    
        'variable': 'ta',
        'plot_projection': 'time_series',
        'depth_type': 'plev',
        'depths':[20000, 85000, 100000], 
        'realization': '1'                                              
        } 

class Test_check_variable:
    def test_variable_is_a_string(self):
        assert ch.check_variable('aaa') == None
        
    def test_variable_is_not_a_string(self):
        with pytest.raises(TypeError):
            ch.check_variable(1)

class Test_check_plot_projection:
    def test_pp_is_not_a_string(self):
        with pytest.raises(TypeError):
            ch.check_plot_projection(1)
    
    def test_pp_is_not_a_possible_value(self):
        with pytest.raises(ValueError):
            ch.check_plot_projection('hello') 
    
    def test_pp_is_a_possible_value(self):
        assert ch.check_plot_projection('mercator') == None  

class Test_check_section: 
    def test_plot_has_depth_type(self):
        plot = {    
            'plot_projection': 'section',
            'depth_type': 'plev',                                           
        } 
        assert ch.check_section(plot) == None
        plot = {    
            'plot_projection': 'mercator',
            'depth_type': 'plev',                                           
        }
        assert ch.check_section(plot) == None
        
    def test_plot_has_no_depth_type(self):         
        plot = {    
            'plot_projection': 'section',                                         
        }
        with pytest.raises(Exception): 
            ch.check_section(plot)
        plot = {    
            'plot_projection': 'mercator',                                          
        }
        assert ch.check_section(plot) == None    
    
class Test_check_bool:
    def test_is_not_bool(self):
        with pytest.raises(TypeError): 
            ch.check_bool('aaa', 'aaa') 
    def test_is_bool(self):
        assert ch.check_bool(True, 'aaa') == None
        
class Test_check_date:
    def test_is_valid_date(self):
        assert ch.check_date('1111') == True
        assert ch.check_date('1111-11') == True
        assert ch.check_date('1111-11-11') == True
    
    def test_not_valid_date(self):                  
        assert ch.check_date('111a') == False
        assert ch.check_date('1111-11-aa') == False
        assert ch.check_date('1111/11/11') == False
        assert ch.check_date('11-11-1111') == False
        assert ch.check_date('1111-1-1') == False
        assert ch.check_date('1111-11-11-11') == False
        
class Test_check_dates:
    def test_dates_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_dates('string','string')
            
    def test_dates_has_wrong_key(self):
        with pytest.raises(ValueError):
            ch.check_dates({'start': '1111-11'},'string')
    
    def test_dates_values_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_dates({'start_date': 1}, 'string')
        with pytest.raises(TypeError): 
            ch.check_dates({'end_date': 1}, 'string')
    
    def test_dates_values_wrong(self):
        with pytest.raises(ValueError):
            ch.check_dates({'start_date': '111'},'string')
        with pytest.raises(ValueError):
            ch.check_dates({'end_date': '1111-11-11-111'},'string')            
        with pytest.raises(ValueError):
            ch.check_dates({'start_date': '111', 'end_date': '1111-11-11'},'string')
        with pytest.raises(ValueError):
            ch.check_dates({'start_date': '1111-11', 'end_date': '1111-'},'string') 
                
    def test_correct_dates(self):
        assert ch.check_dates({'start_date': '1111', 'end_date': '1111-11-11'}, 'string') == None
    
class Test_check_realization:
    def test_real_is_wrong_type(self):
        with pytest.raises(ValueError):
            ch.check_realization('string')
        with pytest.raises(TypeError):
            ch.check_realization(True)
                
    def test_real_is_number_string(self):
        assert ch.check_realization('1') == None
    
    def test_real_is_int(self):    
        assert ch.check_realization(1) == None 

class Test_check_depth_type:
    def test_depth_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_depth_type(1)
    def test_depth_is_right_type(self):
        assert ch.check_depth_type('string') == None

class Test_check_depths:
    def test_depths_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_depths(1)
    def test_the_depths_are_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_depths(['aaa','string'])    
    def test_the_depths_are_right_type(self):
        assert ch.check_depths([20,100]) == None

class Test_check_frequency:
    def test_freq_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_frequency(1)    
    def test_freq_wrong_value(self):
        with pytest.raises(ValueError):
            ch.check_frequency('string')    
    def test_freq_right_value(self):
        assert ch.check_frequency('day') == None
        assert ch.check_frequency('mon') == None        
        assert ch.check_frequency('yr') == None 

class Test_check_scale:
    def test_scale_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_scale('string')      
    def test_scale_is_right_type(self):
        assert ch.check_scale(100) == None    
        assert ch.check_scale(0.01) == None   
        
class Test_check_plot_args:
    def test_pargs_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_plot_args('string')     
    def test_key_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_plot_args({11: True})     
    def test_key_is_wrong_value(self):
        with pytest.raises(ValueError):
            ch.check_plot_args({'string': True})     
    def test_key_is_right_value(self):     
        assert ch.check_plot_args({'fill_continents': True}) == None       
        assert ch.check_plot_args({'draw_parallels': True}) == None
        assert ch.check_plot_args({'draw_meridians': True}) == None

class Test_check_dict:
    def test_dargs_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_dict('string','string')         
    def test_dargs_is_right_type(self):
        assert ch.check_dict({},'string') == None
        
class Test_check_projection_args:
    def test_pargs_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_projection_args('string','string')     
    
    def test_pargs_key_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_projection_args({1:'string'}, 'string')     
    
    def test_pargs_keys_have_wrong_value(self):
        with pytest.raises(ValueError):
            ch.check_projection_args({'string':'string'}, 'string')    
    
    def test_pargs_keys_have_right_value(self):
        assert ch.check_projection_args({'pcolor_args': {}}, 'string') == None
        assert ch.check_projection_args({'ax_args': {}}, 'string') == None
    
    def test_values_are_not_dicts(self):
        with pytest.raises(TypeError):
            ch.check_projection_args('pcolor_args','string')                  
        with pytest.raises(TypeError):
            ch.check_projection_args('ax_args','string')      
    
class Test_check_data_args:  
    def test_dargs_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_data_args('string','string')     
    
    def test_pargs_key_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_data_args({1:'string'}, 'string')     
    
    def test_pargs_keys_have_wrong_value(self):
        with pytest.raises(ValueError):
            ch.check_data_args({'string':'string'}, 'string')    
    
    def test_pargs_keys_have_right_value(self):
        assert ch.check_data_args({'climatology_args': {}}, 'string') == None
        assert ch.check_data_args({'trends_args': {}}, 'string') == None
    
    def test_values_are_not_dicts(self):
        with pytest.raises(TypeError):
            ch.check_data_args('climatology_args','string')                  
        with pytest.raises(TypeError):
            ch.check_data_args('trends_args','string')

class Test_check_plot:
    def test_plot_has_wrong_key(self):
        with pytest.raises(ValueError):
            ch.check_plot({'string':'string'})    
    def test_plots_have_right_keys(self):
        assert ch.check_plot({'variable': 'aa', 'plot_projection': 'mercator'}) == None
        
class Test_check_plots:
    def test_plots_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_plots({})          

    def test_plot_is_wrong_type(self):
         with pytest.raises(TypeError):
            ch.check_plots(['string'])   
    
    def test_plots_are_right_type(self):
        assert ch.check_plots([{}]) == None

class Test_model_run:
    def test_model_run_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_model_run(1)          
    
    def test_model_data_is_not_found(self):
        with pytest.raises(ValueError):
            ch.check_model_run('aaaa')      
    
    def test_model_data_is_found(self):
        assert ch.check_model_run('edr') == None
    
class Test_check_obsroot:
    def test_obsroot_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_obsroot(1)
    
    def test_obsroot_does_not_exist(self):
        with pytest.raises(ValueError):
            ch.check_obsroot('./wrongdirectoryname')  
    
    def test_obsroot_exists(self):
        assert ch.check_obsroot('./') == None    
        
class Test_check_obs:
    def test_obs_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_obs(1)     
    
    def test_obs_key_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_obs({1: 'string'})
     
    def test_obs_value_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_obs({'aa': 1})       
    
    def test_obs_value_does_not_exist(self):
        with pytest.raises(ValueError):
            ch.check_obs({'aa': 'filethatdoesntexist'})     
    
    def test_obs_is_right(self):
        assert ch.check_obs({'aa': 'unittests/test_check.py'}) == None
    
class Test_check_delete:
    def test_delete_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_delete(1)  
                     
    def test_delete_has_wrong_key(self):
        with pytest.raises(ValueError):
            ch.check_delete({'mask': True})     
    
    def test_delete_value_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_delete({'del_mask': 'string'})      
    
    def test_delete_is_right(self):  
        assert ch.check_delete({'del_mask': True}) == None

class Test_check_defaults:
    def test_defaults_is_wrong_type(self):
        with pytest.raises(TypeError):
            ch.check_defaults(1)      
    def test_problem_with_defaults(self):
        with pytest.raises(TypeError):
            ch.check_defaults({1, 'string'})          
    
    def test_defaults_is_valid(self):
        assert ch.check_defaults({'climatology': True}) == None

class Test_check_input:
    def test_problem_with_plots(self):
        model_run = 'edr'
        defaults = {
            'climatology': True,
            }

        plots = {}
        delete = {
          'del_fldmeanfiles': False,
        }         
        obsroot = './'               
        obs = {}         
        with pytest.raises(TypeError):
            ch.check_input(plots, model_run, obsroot, obs, defaults, delete)        
    
    def test_problem_with_model_run(self):
        model_run = 1
        defaults = {
            'climatology': True,
            }

        plots = [
                 {    
                  'variable': 'ta',
                  'plot_projection': 'time_series',                                          
                 }, 
        ]
        delete = {
          'del_fldmeanfiles': False,
        }         
        obsroot = './'               
        obs = {}         
        with pytest.raises(TypeError):
            ch.check_input(plots, model_run, obsroot, obs, defaults, delete)     
    def test_problem_with_obsroot(self):
        model_run = 'edr'
        defaults = {
            'climatology': True,
            }

        plots = [
                 {    
                  'variable': 'ta',
                  'plot_projection': 'time_series',                                          
                 }, 
        ]
        delete = {
          'del_fldmeanfiles': False,
        }         
        obsroot = 1               
        obs = {}         
        with pytest.raises(TypeError):
            ch.check_input(plots, model_run, obsroot, obs, defaults, delete)     
    def test_problem_with_obs(self):
        model_run = 'edr'
        defaults = {
            'climatology': True,
            }

        plots = [
                 {    
                  'variable': 'ta',
                  'plot_projection': 'time_series',                                          
                 }, 
        ]
        delete = {
          'del_fldmeanfiles': False,
        }         
        obsroot = './'               
        obs = []         
        with pytest.raises(TypeError):
            ch.check_input(plots, model_run, obsroot, obs, defaults, delete)     
    def test_problem_with_defaults(self):
        model_run = 'edr'
        defaults = []

        plots = [
                 {    
                  'variable': 'ta',
                  'plot_projection': 'time_series',                                          
                 }, 
        ]
        delete = {
          'del_fldmeanfiles': False,
        }         
        obsroot = './'               
        obs = {}         
        with pytest.raises(TypeError):
            ch.check_input(plots, model_run, obsroot, obs, defaults, delete)     
    def test_problem_with_delete(self):
        model_run = 'edr'
        defaults = {
            'climatology': True,
            }

        plots = [
                 {    
                  'variable': 'ta',
                  'plot_projection': 'time_series',                                          
                 }, 
        ]
        delete = []         
        obsroot = './'               
        obs = {}         
        with pytest.raises(TypeError):
            ch.check_input(plots, model_run, obsroot, obs, defaults, delete)     
    def test_valid_input(self):
        model_run = 'edr'
        defaults = {
            'climatology': True,
            }

        plots = [
                 {    
                  'variable': 'ta',
                  'plot_projection': 'time_series',                                          
                 }, 
        ]
        delete = {
          'del_fldmeanfiles': False,
        }         
        obsroot = None               
        obs = {}         
        assert ch.check_input(plots, model_run, obsroot, obs, defaults, delete) == None    

  
