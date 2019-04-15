# Bruce A. Maxwell
# Fall 2015
# CS 151S Project 3
#
# Updated by Caitrin Eaton on August 25, 2017, for Python3 compliance
#
# Test function for the thermocline function in the file thermocline.py
#
import thermocline

# computes densities for a set of temps and prints them out
def main():

    # some sample temperatures
    temps = [24.47, 23.95, 24.41, 23.81, 19.92, 16.88, 14.06, 11.56, 9.82, 9.13, 8.82]
    depths = [1, 2, 3, 5, 7, 9, 11, 13, 15, 17, 19, 20]

    # call the thermocline function
    depth = thermocline.thermocline_depth( temps, depths )

    # print out the result
    print("Thermocline depth {0:.2f}".format(depth))

    return

if __name__ == "__main__":
    main()
