# Performance page

A performance page generator that lets you host a page which show others how your servers perform for free on Github. It uses [Server Density](https://www.serverdensity.com) to pull metrics from your servers. 


## Demo
Gif of scrolling. 

## Future Features
Open an issue to let us know what kind of features you would like to see. If you are of the creative kind, take a look at the issues and implement a feature!  

    - Save historic data so it can be displayed
    - UI interface interface for configuration instead of yaml


## Installation
The very first thing you should do is to FORK this project. Once you've forked it you can start customizing your settings. 

To be able to get data from your server in the first place you need to monitor your server with Server Density. So go ahead and [sign up for an account](https://www.serverdensity.com) at server density. (Feel free to make PRs to make this work with other monitoring solutions)

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

## Update the data every 24 hours 
When you made sure that your page successfully builds. The next step is to make configurations for Travis. To display the most recent statistics you can use the free service [Nightli.es](https://nightli.es) to continually build your performance page every 24 hours. 

## Configuration
Let's walk through the configuration options that you can make in `conf.yml`. There are two base levels for the yaml file. `general` and `infrastructure`. For the general settings you have the following. 

| Name        | Required | Explanation |
|-------------| -------- | ------------|
| company     | yes      | Your company name |
| header      | yes      | Text below your company name |
| sub-header  | yes      | Smaller text below the header |
| header-image | no      | An image below the header area |
| statuspage  | no       | If you have a statuspage at statuspage.io it'll pull your status from there |
| stack       | no       | A list of your stack which will be displayed at the bottom of the page |
| round       | no       | Rounding of all numbers, defaults to 2 decimals |
| timeframe   | no       | The timeframe you want to display the data from. It defaults to `24` meaning that it will pull data from the last 24 hours. 

For the `infrastructure` heading there are the following settings. 

| Name       | Required  | Explanation |
|----------- | --------- | ----------- |
| title      | yes       | The title of the section |
| title_layout | no      | either left or right, defaults to left |
| subtitle   | no        | A smaller subtitle below the title |
| image      | no        | An image that you can display in the section, requires that you set image_layout |
| image_layout | no      | either left or right |
| size       | no        | The size of the section in percent, defaults to 100 and you can choose from 10, 20, 25, 33, 34, 50, 60, 66, 67, 75, 80, 90, 100 |
| group      | maybe     | The group name in Server Density, either tag or group is required |
| tag        | maybe     | The tag name in Server Density, either tag or group name is required |
| bubble-description | no | A description that shows up as a bubble above the metric |

Inside the `infrastructure` heading there is a `metrics` heading. The `metrics` heading takes a yaml list where you can make the following settings.  

| Name       | Required | Explanation |
|----------  | -------- | ----------- |
| metrickey  | yes      | After having done `make available`, you'll see all the possible keys, this is where you put it. | 
| calculation | yes     | A yaml list of ways to make calculations for the metric. Possible values are `average`, `sum`, `max`, `median`, `min` |
| *your_calc*_title | - | if you used average as a calculation method, it should be `average_title` |
| *your_calc*_unit | -  | if you used average as a calculation method, it should be `average_unit` |
| *your_calc*_stat | -  | if you used average as a calculation method, it should be `average_stat`, this is useful for dummy if you quickly want to see how things look when using `make generate_dev` |
| style      | no       | uses the different modules defined in `index.html`. The default style is `circle_frame`

### Template
If you want to make any changes to the page itself you can make the changes in the `index.html` file located in the templates folder 

### Config file
Here is an example of a [configuration file](https://github.com/serverdensity/performance-page/blob/master/conf_dev.yml) and this is the [configuration file](https://github.com/serverdensity/performance-page/blob/master/conf.yml) we used to make our page. 

### Use a subdomain

If you want to use your own domain to host your performance page, you'll need to create a CNAME file and set up a CNAME record pointing to that page with your DNS provider. There already is a CNAME file in the source folder. Change this to your own domain. 

If you have e.g. the domain `mydomain.com`, your GitHub repo is `my-repo` and you want your status page to be reachable at `performance.mydomain.com`

- Change the `CNAME` file in the source folder to 

        performance.mydomain.com
    
- Go to your DNS provider and create a new CNAME record pointing to your

          Name          Type      Value 
          performance   CNAME     myusername.github.io/my-repo

See [Using a custom domain with GitHub Pages](https://help.github.com/articles/custom-domain-redirects-for-github-pages-sites/) for more info.

## Modules

### Explanation of they work

Some code. 

### Gallery

Images of modules


<a name="myfootnote1">1</a>: It assumes that every device in your group uses the same metrics, so it only checks the first device to speed things up. 
