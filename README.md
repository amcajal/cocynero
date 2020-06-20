<!--- PROJECT LOGO --->
![project_logo](https://github.com/amcajal/cocynero/blob/master/project/doc/media/cocynero_readme_logo.png)

<!--- BADGES AND SHIELDS --->
![License](https://img.shields.io/badge/License-GPL%20v3.0-blue.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)

<!--- PROJECT SUMMARY/OVERVIEW --->
Cocynero (a pun between word "cocinero" -chef, cooker in Spanish- and the Y on Python)
is both:
- A dataset of kitchen recipes and ingredients, all in plain text-old CSV format.
- The software -written in Python- to work with such dataset(s)

The goal of the project is to provide the means (data and software) to ease
the "Weekly menu" generation, and all related rituals, for anyone who needs it; or simply put: to avoid
the "What I'm gonna eat today?" question, or the "I forgot the shopping list" lament.

The Cocynero software, using the data contained in the datasets is able to do things like this:
- Choose in a random fashion 14 recipes for the Weekly menu (2 per day -lunch and supper-, from Monday to Sunday)
- Generate the shopping list for the previous generated menu
- Search recipes with specific ingredients

Cocynero does not only provides the software to work with the datasets, but also
software to generate such datasets (to some extent).

DISCLAIMER:
The recipes dataset is not included here, at least for now. The reason for this
is that it is generated through Web Scrapping, and unfortunately, it is very
easy to track the data back to its original source -with COPYRIGHT.

Ingredients dataset is generated from the recipes dataset, but its content
cannot be traced to nothing (is just a list of ingredients names and other
fields), so it is included with no worries.

For technical details and more info, visit the [Wiki of the project](https://github.com/amcajal/cocynero/wiki)

---

## Index
1. [Quickstart](#quickstart)
2. [Contributions](#contributions)
3. [License](#license)
4. [Contact](#contact)

---

## Quickstart

- Clone the repository: 
```
$> git clone https://github.com/amcajal/cocynero.git
```

- Move to the home folder and execute "setup.bsh"
```
$> cd <whatever>/cocynero
$> bash setup.bsh
```

And the fun starts.

[Back to index](#index)


## License

About **Cocynero**:

Alberto Martin Cajal is the original author of **Cocynero**. 
**Cocynero** is released under GNU GPL version 3.0 license. Check LICENSE file for a full version of it, or visit the [official GNU web page](https://www.gnu.org/licenses/gpl-3.0.en.html)

[Back to index](#index)


## Contributions
**Cocynero** is open to contributions! [Check the related page at the Wiki of the project](https://github.com/amcajal/cocynero/wiki/Page-9:-Contributions)

[Back to index](#index)


## Contact
Alberto Martin Cajal at:
 
- Gmail: amartin.glimpse23@gmail.com (amartin DOT glimpse23 AT gmail DOT com)
- [Blogspot](http://glimpse-23.blogspot.com.es/)
- [LinkedIn](https://es.linkedin.com/in/alberto-martin-cajal-b0a63379)
- Twitter: @amartin_g23

[Back to index](#index)

---

#### This project has been created trying to make it useful. This project has been created in order to learn new things. But over all, this project has been created because it is fun. As Isaac Asimov said:

*The most exciting phrase to hear in science, the one that heralds new discoveries, is not 'Eureka' but 'That's funny...'*
