const BASE_URL = 'http://localhost:5000'

/**
 * The Search class represents the current search data. 
 * There are helper methods to generate different graphs using the data.
 */

class Search {
  constructor(responseObj) {
    this.deaths = responseObj.deaths
    this.cases = responseObj.cases
    this.dates = responseObj.dates

    // these are set by default, not passed in by the constructor
    this.days = 16
  }

  /**
   * Create and return a new search.
   * Makes POST request to backend and returns newly-created search
   */

  static async create(location, date) {
    const response = await axios.post(`${BASE_URL}/search`, {
      "location": location,
      "date": date
    })

    if (!response.data.cases || !Array.isArray(response.data.cases)) {
      throw new Error('Invalid data from server')
    }

    const newSearch = new Search(response.data)
    
    return newSearch

  // request to post to searches to save data if user is logegd in
}


// Method for showing first graph with 16 days from date selected

// Method for extending graph to full graph with all days from date selected to today's date

// Method for adding another graph with deaths as well.
  generateGraph(div) {
    let chart = c3.generate({
      bindto: div,
      data: {
        x: 'x',
        xFormat: '%m-%d-%y',
        columns: [
          ['x', ...this.dates.slice(0, this.days)],
          ['cases', ...this.cases.slice(0, this.days)]
        ],
      },
      grid: {
        x: {
          lines: [
            {value: this.dates[5], text: '5 days'},
            {value: this.dates[10], text: '10 days'},
            {value: this.dates[15], text: '15 days'},
          ]
        }
      },
      axis: {
        x: {
          type: 'timeseries',
          tick: {
            format: '%m-%d'
          },
          y2: {
            show: true
          }
        }
      }
    })

    return chart
  }

  showAllDates(graph) {
    graph.flow({
      columns: [
        ['x', ...this.dates.slice(this.days)],
        ['cases', ...this.cases.slice(this.days)]
      ],
      duration: 1500,
      length: 0
    })
  }
}
