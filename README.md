# electionformfiller
A service to fill out nomination papers and send them to candidates

# Behaviour
When you http GET this service it will fill in a pdf with your query parameters and email the pdf to the provided email address

##Query parameters
    'addr_city'
    'addr_first'
    'addr_second'
    'firstname'
    'DoB_d'
    'DoB_m'
    'DoB_y'
    'commonforename'
    'commonsurname'
    'othernames'
    'surname'
    'addr_postcode'
    'constituency'
    'email' # this is the email that the pdf will be sent to

## Deploy to heroku

    heroku create

### Configure
    BUILDPACK_URL:   https://github.com/ddollar/heroku-buildpack-multi.git
    LD_LIBRARY_PATH: /app/vendor/pdftk/lib
    PATH:            /app/.heroku/python/bin:/usr/local/bin:/usr/bin:/bin:/app/vendor/pdftk/bin
    MANDRILL_USER:   mandrill settings
    MANDRILL_PASS:   
    MANDRILL_FROM:   where your emails are sent from

Then cross your fingers and run

    git push heroku master

## Try it out
    curl "http://electionformfiller.herokuapp.com/?constituency=Camberwell&firstname=Giovanni&surname=Charles&email=[someone]@someone.com"
