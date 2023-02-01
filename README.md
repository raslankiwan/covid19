
{% if False %}

# Introduction

This app provides statistics for Covid 19 for users. The user can subscribe to one or more countries.

# Usage

To use the APIs, import Covid19.postman_collection.json into Postman, and Initialize "token" as a global variable for the tests to work correctly.


First, use the Register API to create a user, provide it with the username and password for the user.


"Add country" API provides the ability to subscribe to a country.


"Top countries" API can be used to get the top 3 countries from the user's subscribed countries based on the status supplied in the request parameter ("deaths"/"confirmed"). The result is sorted in descending order.
The number of countries can be changed by passing the limit parameter


"Death Percentage" API returns the deaths to confirmed cases ration for a given country.


"User Statistics" API Returns the info for all the countries the user subscribed for.
 
#
