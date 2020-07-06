 // The Search class represents the current search data. 
 // There are helper methods to generate different graphs using the data.
class Search {
  constructor(responseObj, location, date) {
    this.deaths = responseObj.deaths
    this.cases = responseObj.cases
    this.dates = responseObj.dates
    this.created_at = responseObj.created_at
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
    if (response.data === 'not usa') {
      throw new Error('Please select a location in the US.')
    } else if (response.data === 'no county') {
      throw new Error("Can't find county data for the requested location.")
    } else if (response.data === 'invalid date') {
      throw new Error('Please select an earlier date.')
    } else if (response.data === 'no data') { 
      throw new Error('Unfortunately we have no data for the requested search.')
    } else if (response.data === "Can't save search right now." || !response.data.cases || !Array.isArray(response.data.cases)) {
      throw new Error('An unexpected error has occured, please try again later.')
    }

    const newSearch = new Search(response.data, location, date)
    
    return newSearch

  // request to post to searches to save data if user is logegd in
}

  async save() {
    const response = await axios.post('/search/save', {
      "location": this.location.replace(', US', ''),
      "date": this.date,
      "dates": this.dates.toString(),
      "cases": this.cases.toString(),
      "deaths": this.deaths.toString(),
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


  // TODO: Customize tooltip to show case/death increase.
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