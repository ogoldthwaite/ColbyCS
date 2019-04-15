# Bruce A. Maxwell
# Fall 2015
# CS 151S Project 3
#
# Updated by Caitrin Eaton on August 25, 2017, for Python3 compliance
#
# Test function for the density function in the file thermocline.py
#
import thermocline

# computes densities for a set of temps and prints them out
def main():

    # some sample temperatures
    temps = [24.47, 23.95, 24.41, 23.81, 19.92, 16.88, 14.06, 11.56, 9.82, 9.13, 8.82]

    # call the density function
    rhos = thermocline.density( temps )

    # print out the temps and corresponding densities
    for i in range(len(temps)):
        print("{0:.2f} -> {1:.2f}".format(temps[i], rhos[i]))

    return

if __name__ == "__main__":
    main()
