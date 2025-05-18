import json
import sys
import os

class BettingConfig:


    def __init__(self, 
                 conf_alta=0.80,
                 conf_media_min=0.70,
                 conf_media_max=0.79,
                 conf_baixa_min=0.55,
                 conf_baixa_max=0.69,
                 stake_base=20.00,
                 stake_alta_pct=100,
                 stake_media_pct=50,
                 stake_baixa_pct=25):
        
        self.conf_alta = conf_alta
        self.conf_media_min = conf_media_min
        self.conf_media_max = conf_media_max
        self.conf_baixa_min = conf_baixa_min
        self.conf_baixa_max = conf_baixa_max
        
        self.stake_base = stake_base
        self.stake_alta_pct = stake_alta_pct
        self.stake_media_pct = stake_media_pct
        self.stake_baixa_pct = stake_baixa_pct
    def get_base_path(self):
        import os

        # get the current working directory
        current_working_directory = os.getcwd()
        return current_working_directory

    def get_generated_path(self):
        """Get the correct path to generated files"""
        base = self.get_base_path()
        path = os.path.join(base,'app','generated')
        return path
    def calibrar_confianca(self, prob):
        """Determine confidence level based on probability"""
        if prob >= self.conf_alta:
            return 'alta'
        elif prob >= self.conf_media_min:
            return 'média'
        elif prob >= self.conf_baixa_min:
            return 'baixa'
        else:
            return 'fraca'
    
    def calcular_stake(self, confidence_level):
        """Calculate stake amount based on confidence level"""
        if confidence_level == 'alta':
            return self.stake_base * (self.stake_alta_pct / 100)
        elif confidence_level == 'média':
            return self.stake_base * (self.stake_media_pct / 100)
        elif confidence_level == 'baixa':
            return self.stake_base * (self.stake_baixa_pct / 100)
        return 0  # No bet for 'fraca' confidence
    
    def to_dict(self):
        """Serialize config to dictionary"""
        return {
            'conf_alta': self.conf_alta,
            'conf_media_min': self.conf_media_min,
            'conf_media_max': self.conf_media_max,
            'conf_baixa_min': self.conf_baixa_min,
            'conf_baixa_max': self.conf_baixa_max,
            'stake_base': self.stake_base,
            'stake_alta_pct': self.stake_alta_pct,
            'stake_media_pct': self.stake_media_pct,
            'stake_baixa_pct': self.stake_baixa_pct,
            'nivel_alta':self.conf_alta,
            'nivel_media':self.conf_media_min,
            'nivel_baixa':self.conf_baixa_min,
            'stake_alta':self.stake_alta_pct,
            'stake_media':self.stake_media_pct,
            'stake_baixa':self.stake_baixa_pct
        }
    
    
    def from_dict(self, config_dict):
        """Robust dictionary conversion that handles both GUI and native formats"""
        # First check if it's a GUI-style config
        
        gui_config = config_dict
        
        self.conf_alta=gui_config['conf_alta']
        self.conf_media_min=gui_config['conf_media_min']
        self.conf_media_max=gui_config['conf_media_max']
        self.conf_baixa_min=gui_config['conf_baixa_min']
        self.conf_baixa_max=gui_config['conf_baixa_max']
        self.stake_base=20.00  # Default from class
        self.stake_alta_pct=gui_config['stake_alta_pct']
        self.stake_media_pct=gui_config['stake_media_pct']
        self.stake_baixa_pct=gui_config['stake_baixa_pct']
        return {
            'conf_alta':self.conf_alta,
            'conf_media_min':self.conf_media_min,
            'conf_media_max':self.conf_media_max,
            'conf_baixa_min':self.conf_baixa_min,
            'conf_baixa_max':self.conf_baixa_max,
            'stake_base':20.0,
            'stake_alta_pct':self.stake_alta_pct,
            'stake_media_pct':self.stake_media_pct,
            'stake_baixa_pct':self.stake_baixa_pct
        }
        
    def save_config(self,config, path):
        """Save configuration to JSON file"""
        with open(os.path.join(self.get_generated_path(),'grisamanus_config.json')) as f:
            json.dump(config.to_dict(), f, indent=2)
        self.load_config()

    def load_config(self):
        """Load configuration from JSON file"""
        with open(os.path.join(self.get_generated_path(),'grisamanus_config.json')) as f:
            conf = json.load(f)
            self.from_dict(conf)
            return conf