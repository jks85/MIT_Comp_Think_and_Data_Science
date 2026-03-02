# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: jks85
# Collaborators (discussion):
# Time:

# see lines 392 and 404 for model and plot generation

import pylab
import re



# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """

    model_coefficients = []
    for degree in degs:
        model_coefficients.append(pylab.polyfit(x,y,degree))

    return model_coefficients

# print(generate_models(pylab.array([1961, 1962, 1963]),
# pylab.array([-4.4, -5.5, -6.6]), [1, 2]))

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """

    # compute residuals
    sq_residuals = (y - estimated)**2
    ssr = sq_residuals.sum()

    # compute deviations from mean
    # y_means = y.mean()*pylab.ones(y.size)
    # sq_mean_devs = (y-y_means)**2
    sq_mean_devs = (y - y.mean())**2
    sst = sq_mean_devs.sum()
    r_sq = 1 - ssr/sst

    return r_sq

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # print(f"Evaluating training data using {len(models)} models")
    # get degrees
    degrees = [len(model) - 1 for model in models]

    y_estimates= []

    # create model estimates
    for model in models:
        y_estimates.append(pylab.polyval(model, x))

    # compute r^2 vals and se_slope ratios
    r_sq_vals = []
    se_slope_ratios = []

    for i in range(len(y_estimates)):
        r_sq_vals.append(round(r_squared(y, y_estimates[i]), 3))
        se_slope_ratios.append(se_over_slope(x, y, y_estimates[i], models[i]))

    # create plots
    # currently uses index of r^2 val. could refactor
    for r in r_sq_vals:
        r_index = r_sq_vals.index(r)
        se_slope_ratio_index = r_index
        degree = degrees[r_index]
        title = (f"Degree {degree} fit, R^2 = {r} \n "
                 f"Standard error to slope ratio: {round(se_slope_ratios[se_slope_ratio_index],3)}")

        pylab.plot(x,y,'bo')
        pylab.plot(x,y_estimates[r_index],'r',
                   label =f"")
        pylab.legend(loc = 'upper left')
        pylab.title(title)
        pylab.xlabel("Year")
        pylab.ylabel("Temperature (Celsius)")
        pylab.show()


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    city_avg = []
    for year in years:
        city_temps = pylab.array([])
        for city in multi_cities:
            # check if year exists
            if climate.rawdata[city][year]:
                year_temps = climate.get_yearly_temp(city,year)
                city_temps = pylab.concatenate((city_temps,year_temps))
        city_avg.append(city_temps.mean())

    return pylab.array(city_avg)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # Note: in the unit tests the parameter y is a list not a pylab array

    moving_avgs = []
    y = pylab.array(y)
    for i in range(y.size):
        temp_mean = 0
        if i < (window_length - 1):
            temp_mean = y[0:(i+1)].mean()
        else:
            temp_mean = y[(i - window_length + 1):(i+1)].mean()
        moving_avgs.append(temp_mean)

    return pylab.array(moving_avgs)


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    sq_devs = (y-estimated)**2
    mean_sq_devs = sq_devs.sum()/sq_devs.size
    return mean_sq_devs**0.5

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    city_std_devs = []
    # get avg temps across cities for each day in a year
    # compute std dev of temps for that year
    # implementation assumes no missing data for dates in years...

    for year in years:
        is_leap_year = True if year % 4 == 0 else False
        temps_array = pylab.zeros(366) if is_leap_year else pylab.zeros(365)
        for city in multi_cities:
            yearly_temps = climate.get_yearly_temp(city,year)
            for i in range(len(yearly_temps)):
                temps_array[i] += yearly_temps[i]
        temps_array = temps_array/len(multi_cities)
        city_std_devs.append(temps_array.std())

    return pylab.array(city_std_devs)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # print(f"Evaluating training data using {len(models)} models")
    # get degrees
    degrees = [len(model) - 1 for model in models]

    y_estimates = []

    # create model estimates
    for model in models:
        y_estimates.append(pylab.polyval(model, x))

    # compute rmse vals
    rmse_vals = []

    for i in range(len(y_estimates)):
        rmse_vals.append(round(rmse(y, y_estimates[i]), 3))

    # create plots
    # currently uses index of rmse val. could refactor
    for r in rmse_vals:
        r_index = rmse_vals.index(r)
        degree = degrees[r_index]
        title = f"Degree {degree} fit, RMSE = {r}"

        pylab.plot(x, y, 'bo')
        pylab.plot(x, y_estimates[r_index], 'r',
                   label=f"")
        pylab.legend(loc='upper left')
        pylab.title(title)
        pylab.xlabel("Year")
        pylab.ylabel("Temperature (Celsius)")
        pylab.show()



if __name__ == '__main__':



    # Part A.4
    ### INVESTIGATING TRENDS ###

    climate = Climate("data.csv")
    city = "NEW YORK"


    # get existing training years
    years_train = [year for year in climate.rawdata[city].keys() if year in TRAINING_INTERVAL]

    ### JAN 10TH NYC YEARLY TEMP ANALYSIS ###
    month = 1   # January
    day = 10

    # compute temps
    temps_train = [climate.get_daily_temp(city, month, day, year) for year in TRAINING_INTERVAL]
    temps_test = [climate.get_daily_temp(city, month, day, year) for year in TESTING_INTERVAL]

    # create pylab arrays
    years_train = pylab.array(years_train)
    temps_train = pylab.array(temps_train)
    # temps_test = pylab.array(temps_test)

    # # create model and plot
    linear_model_jan10 = generate_models(years_train, temps_train, [1])
    # evaluate_models_on_training(years_train,temps_train,linear_model_jan10) # evaluate and plot models

    ### NYC AVG YEARLY TEMP ANALYSIS ###

    yearly_temps_train = [climate.get_yearly_temp(city, year) for year in climate.rawdata[city]
                          if year in TRAINING_INTERVAL]
    yearly_mean_temps_train = [temp_array.mean() for temp_array in yearly_temps_train]

    yearly_mean_temps_train = pylab.array(yearly_mean_temps_train)

    # # create model and plot
    linear_model_yearly = generate_models(years_train, yearly_mean_temps_train, [1])
    # evaluate_models_on_training(years_train, yearly_mean_temps_train, linear_model_yearly)  # evaluate and plot models


    # Part B

    # create model for avg city temp
    city_temp_avg = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    linear_model_partB = generate_models(years_train, city_temp_avg, [1])
    # evaluate_models_on_training(years_train,city_temp_avg, linear_model_partB)  # evaluate and plot models

    # Part C

    # create model for moving average of avg city temp (5 year avg)
    window_length = 5
    city_temp_moving_avg = moving_average(city_temp_avg,window_length)
    linear_model_partC = generate_models(years_train, city_temp_moving_avg,[1])
    # evaluate_models_on_training(years_train, city_temp_moving_avg,linear_model_partC)   # evaluate and plot models


    # Part D.2
    # use moving average info from part C
    test_models = generate_models(years_train, city_temp_moving_avg,[1,2,20])
    # evaluate_models_on_training(years_train, city_temp_moving_avg,test_models)

    # Part E

    # get test years & compute moving averages
    # using model found in part D for testing

    years_test = [year for year in climate.rawdata[city].keys() if year in TESTING_INTERVAL]
    years_test = pylab.array(years_test)
    city_temp_test_avg = gen_cities_avg(climate, CITIES, TESTING_INTERVAL)
    city_temp_moving_test_avg = moving_average(city_temp_test_avg, window_length)
    # evaluate_models_on_testing(years_test, city_temp_moving_test_avg, test_models)  # evaluate and plot models

    # compute statistics of 5 year moving avg temp for comparison to RMSE
    city_temp_moving_test_avg.mean() # 16.94 degrees Celsius
    city_temp_moving_test_avg.min()  # 16.76 degrees Celsius
    city_temp_moving_test_avg.max()  # 17.09 degrees Celsius

    # std dev of temps for cities in training interval
    std_devs = gen_std_devs(climate,CITIES,TRAINING_INTERVAL)

    # 5 year moving avg of std devs
    std_dev_moving_avg = moving_average(std_devs, window_length)
    std_dev_model = generate_models(years_train, std_dev_moving_avg,[1])
    # evaluate_models_on_training(years_train,std_dev_moving_avg, std_dev_model)




