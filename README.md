# Performance page

A performance page generator that lets you host a page which show others how your servers perform for free on Github. It uses [Server Density](https://www.serverdensity.com) to pull metrics from your servers. 


## Demo
Gif of scrolling. 

## Future Features
Open an issue to let us know what kind of features you would like to see. If you are of the creative kind, take a look at the issues and implement a feature!  


## Installation
To be able to get data from your server in the first place you need to monitor your server with Server Density. So go ahead and [sign up for an account](https://www.serverdensity.com) at server density. 

The next step is to start configuring your `conf.yml` to be able to fetch data. Use `conf_dev.yml` as a starting point for your configurations. The first step would be to fill in all the groups or tags that you want to monitor. Then run `make available`. That will create a file `available.md` with all the metrics each group or tag has<sup>[1](#myfootnote1)</sup>. 

This is what it will look like. From here you can see what metrics you find interesting and then go on and copy the metrickey to each metrics in `conf.yml` 
```
    # Available metrics for all your groups

    ##API Load Balancers
    ###Top Processes python (sd-agent) Processes
    metrickey: topProcesses.python (sd-agent).p

    ###Top Processes python (sd-agent) CPU
    metrickey: topProcesses.python (sd-agent).c

    <snip>
```

Once you're happy with the configuration you can run `make generate` to generate the performance page. This will create an output folder where `index.html` exists which is your performance page. Go on, take a look at what your brand new performance page looks like! 

To get the layout all fancy and look good, a faster option is to not work with data that you fetch each time. Just run `make generate_dev` to generate the template without live data.

## Configuration

### Template
The main template file. 

### Config file
Link to config file example. 

## Modules

### Explanation of they they work

Some code. 

### Gallery

Images of modules


### Use a subdomain

(needs rewriting)

If you want to use your own domain to host your status page, you'll need to create a CNAME file
in your repository and set up a CNAME record pointing to that page with your DNS provider.

If you have e.g. the domain `mydomain.com`, your GitHub username is `myusername` and you want 
your status page to be reachable at `status.mydomain.com`


- Create a `CNAME` file in the root of your repository

        status.mydomain.com
    
- Go to your DNS provider and create a new CNAME record pointing to your

  
          Name     Type      Value 
          status   CNAME     myusername.github.io

See [Using a custom domain with GitHub Pages](https://help.github.com/articles/using-a-custom-domain-with-github-pages/) 
for more info.

<a name="myfootnote1">1</a>: It assumes that every device in your group uses the same metrics, so it only checks the first device to speed things up. 
