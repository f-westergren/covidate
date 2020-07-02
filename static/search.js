 // The Search class represents the current search data. 
 // There are helper methods to generate different graphs using the data.
class Search {
  constructor(responseObj, location, date) {
    this.deaths = responseObj.deaths
    this.cases = responseObj.cases
    this.dates = responseObj.dates
    this.location = location
    this.date = date

    // these are set by default, not passed in by the constructor
    this.days = 16
  }

  // Create and return a new search.
  // Makes POST request to backend and returns newly-created search
  static async create(location, date) {
    console.log('DATE', date)
    const response = await axios.post('/search', {
      "location": location,
      "date": date
    })

    if (!response.data.cases || !Array.isArray(response.data.cases)) {
      throw new Error('Invalid data from server')
    }

    const newSearch = new Search(response.data, location, date)
    
    return newSearch

  // request to post to searches to save data if user is logegd in
}

  static async save() {
    await axios.post('/search/save', {
      "location": this.location,
      "date": this.date,
      "dates": this.dates,
      "cases": this.cases,
      "deaths": this.deaths,
    })
  }

  // TODO: Add SELECT points with numbers for every 5 days.
  // TODO: Customize tooltip to show case/death increase.
  // TODO: Fix decimals in y axis
  // TODO: Fix only cities and counties in US.


  // Method for generating chart from data and append to selected div.
  generateChart(div, covidData=this.cases, label='cases') {

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
          [label, ...covidData.slice(0, this.days)]
        ]
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
                  return (parseInt(d) == d) ? d : null;
              }
          }
        }
      }
    })

    return chart
  }

   // TODO: Add animation to when reverting graph.

  // Method for generating chart from data and append to selected div.
  showAllDates(chart) {
    // Check to see if currently showing deaths or cases and set data accordingly
    let legend = document.querySelector('.c3-legend-item').textContent 
    let data = (legend == 'deaths') ? this.deaths : this.cases

    // Render chart
    chart.flow({
      columns: [
        ['x', ...this.dates.slice(this.days)],
        [legend, ...data.slice(this.days)]
      ],
      duration: 1500,
      length: 0
    })
  }
    
  // Method for rendering 15 dates in chart
  showFifteenDates(chart) {
    // Check to see if currently showing deaths or cases and set data accordingly
    let legend = document.querySelector('.c3-legend-item').textContent
    let data = (legend == 'deaths') ? this.deaths : this.cases

    // Render chart
    chart.load({
      unload: true,
      columns: [
        ['x', ...this.dates.slice(0, this.days)],
        [legend, ...data.slice(0, this.days)]
      ],
    })
  }

  // Method for rendering deaths in chart
  showDeaths(all=false) {
    // Check to see if currently showing all dates or 15 dates and set data accordiongly
    let data = all ? ['deaths', ...this.deaths] : ['deaths', ...this.deaths.slice(0, this.days)]
    chart.load({
      unload: true,
      columns: [
        data       
      ]
    })
  }

  // Method for rendering cases in chart
  showCases(all=false) {
    // Check to see if currently showing all dates or 15 dates and set data accordiongly
    let data = all ? ['cases', ...this.cases] : ['cases', ...this.cases.slice(0, this.days)]
    chart.load({
      unload: true,
      columns: [
        data       
      ]
    })
  }
}