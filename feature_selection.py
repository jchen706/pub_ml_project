import pandas as pd
import statsmodels.api as sm

class FeatureSelection(object):
    def __init__(self):
        pass

    @staticmethod
    def forward_selection(data, target, significance_level=0.05): # 9 pts
        '''
        Implement forward selection using the steps provided in the notebook.
        You can use sm.OLS for your regression model.
        Do not forget to add a bias to your regression model. A function that may help you is the 'sm.add_constants' function.
        
        Args:
            data: data frame that contains the feature matrix
            target: target feature to search to generate significant features
            significance_level: the probability of the event occuring by chance
        Return:
            forward_list: list containing significant features (in order of selection)

        '''
        N,D = data.shape
        lab = data.columns
        select = []
        pvalues = []
        for num in range(D):
            pvalues = []
            for i in lab:
                if not i in select:
                    data_con = sm.add_constant(data[select + [i]])
                    model = sm.OLS(target, data_con)
                    result = model.fit()
                    pvalues.append((result.pvalues[i],i))
            if min(pvalues)[0] >= significance_level:
                break;
            else:
                select.append(min(pvalues)[1])
        return select
    
        
        
    @staticmethod
    def backward_elimination(data, target, significance_level = 0.05): # 9 pts
        '''
        Implement backward selection using the steps provided in the notebook.
        You can use sm.OLS for your regression model.
        Do not forget to add a bias to your regression model. A function that may help you is the 'sm.add_constants' function.

        Args:
            data: data frame that contains the feature matrix
            target: target feature to search to generate significant features
            significance_level: the probability of the event occuring by chance
        Return:
            backward_list: list containing significant features
            removed_features = list containing removed features (in order of removal)
        '''
        N,D = data.shape
        select = []
        lab = data.columns
        for num in range(D):
            con = list(set(lab) - set(select))
            data_con = sm.add_constant(data[con])
            model = sm.OLS(target, data_con)
            result = model.fit()
            if result.pvalues.max() <= significance_level:
                back = (result.pvalues.drop('const').sort_values()).index.values
                return back, select
            else:
                select.append(result.pvalues.idxmax())
        back = (result.pvalues.drop('const').sort_values()).index.values
        return back ,select
