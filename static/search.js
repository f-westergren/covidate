 // The Search class represents the current search data. 
 // There are helper methods to generate different graphs using the data.
class Search {
  constructor(responseObj, location, date) {
    this.deaths = responseObj.deaths
    this.changeDeaths = responseObj.change_deaths
    this.cases = responseObj.cases
    this.changeCases = responseObj.change_cases
    this.dates = responseObj.dates
    this.createdAt = responseObj.created_at
    this.id = responseObj.id                                                                                                                                                                
    this.location = location
    this.date = date

    // these are set by default, not passed in by the constructor
    this.days = 16
  }

  // Create and return a new search.
  // Makes POST request to backend and returns newly-created search
  static async create(location, date) {
      const response = await axios.post('/search', {
        "location": location,
        "date": date,
        "saved": false
    })
    const newSearch = new Search(response.data, location, date)
    return newSearch
}

  async save(description=undefined) {
    const response = await axios.post('/search/save', {
      "location": this.location,
      "date": this.date,
      "dates": this.dates.toString(),
      "cases": this.cases.toString(),
      "change_cases": this.changeCases.toString(),
      "deaths": this.deaths.toString(),
      "change_deaths": this.changeDeaths.toString(),
      "description": description
    })
    return response
  }

  static async load(search_id) {
    const response = await axios.get(`/search/load?id=${search_id}`)
    const savedSearch = new Search(response.data, response.data.location, response.data.date)

    return savedSearch
  }

  async delete() {
    const response = await axios.post(`/search/${this.id}/delete`)

    return response.data
  }

  // Method for generating chart from data and append to selected div.
  generateChart(div, cases=this.cases, deaths=this.deaths, label='cases') {

    // Add datelines with grid line every five days
    let dateLines = []
    for (let i = 1;i < this.dates.length;i++) {
      if (i % 5 === 0) {
        dateLines.push({'value': this.dates[i], 'text': `${i} days`})
      }
    }

    // Generate chart
    let chart = c3.generate({
      bindto: div,
      data: {
        x: 'x',
        xFormat: '%m-%d-%y',
        columns: [
          ['x', ...this.dates.slice(0, this.days)],
          [label, ...cases.slice(0, this.days)],
          ['change', ...this.changeCases.slice(0, this.days)],
        ],
        hide: ['change'],
        axes: {
          label: 'y1',
          change: 'y2'
        }
      },
      grid: {
        x: {
          lines: dateLines
        }
      },
      axis: {
        x: {
          type: 'timeseries',
          tick: {
            format: '%m/%d'
          }
        },
        y: {
          tick: {
              format: function (d) {
                  return (parseInt(d) == d) ? d : null; // Remove decimals on y axis
              }
          }
        },
        y2: {
          tick: {
            format: function (d) {
                return (parseInt(d) == d) ? d : null; // Remove decimals on y axis
            }
          },
          show: true
        }
      },
      legend: {
        item: { onclick: function () {} }
      },
      tooltip: {
        format: {
            value: function (value, ratio, id) {

              let diff = 0
              if (id === 'cases') {
                diff = value - cases[0]
                return `${value} (total increase of ${diff} ${id})`
              } else if (id === 'deaths') {
                diff = value - deaths[0]
                return `${value} (total increase of ${diff} ${id})`
              }

              return `Daily change: ${value}`
            }
        }
    }
    })

    return chart
  }

  // Method for generating chart from data and append to selected div.
  showAllDates(chart) {
    // Check to see if currently showing deaths or cases and set data accordingly
    let legend = document.querySelector('.c3-legend-item').textContent 
    let data, changeData;

    if (legend === 'deaths') {
      data = this.deaths
      changeData = this.changeDeaths
    } else {
      data = this.cases
      changeData = this.changeCases
    }

    // Render chart
    chart.flow({
      unload: false,
      columns: [
        ['x', ...this.dates.slice(this.days)],
        [legend, ...data.slice(this.days)],
        ['change', ...changeData.slice(this.days)]
      ],
      duration: 1500,
      length: 0
    })
  }
    
  // Method for rendering 15 dates in chart
  showFifteenDates(chart) {
    // Check to see if currently showing deaths or cases and set data accordingly
    let legend = document.querySelector('.c3-legend-item').textContent 
    let data, changeData;

    if (legend === 'deaths') {
      data = this.deaths
      changeData = this.changeDeaths
    } else {
      data = this.cases
      changeData = this.changeCases
    }

    // Render chart
    chart.load({
      unload: true,
      columns: [
        ['x', ...this.dates.slice(0, this.days)],
        [legend, ...data.slice(0, this.days)],
        ['change', ...changeData.slice(0, this.days)]
      ],
    })
  }

  // Method for rendering deaths in chart
  showDeaths(all=false, chart) {
    console.log('DEATHS', this.changeDeaths, this.changeCases)
    // Check to see if currently showing all dates or 15 dates and set data accordiongly
    let data = all ? 
      [['deaths', ...this.deaths], ['change', ...this.changeDeaths]] 
      : 
      [['deaths', ...this.deaths.slice(0, this.days)], ['change', ...this.changeDeaths.slice(0, this.days)]]
    chart.load({
      unload: true,
      columns: 
        data       
    })
  }

  // Method for rendering cases in chart
  showCases(all=false, chart) {
    // Check to see if currently showing all dates or 15 dates and set data accordiongly
    let data = all ? 
      [['cases', ...this.cases], ['change', ...this.changeCases]] 
      : 
      [['cases', ...this.cases.slice(0, this.days)], ['change', ...this.changeCases.slice(0, this.days)]]
    chart.load({
      unload: true,
      columns: 
        data       
    })
  }
}