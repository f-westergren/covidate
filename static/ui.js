// global currentUser variable
let currentSearch = null
let chart = null
let showLoader = false
let showDates = false

const toggleAllDates = (e) => {
  if (!showDates) {
    currentSearch.showAllDates(chart)
    e.target.innerText = 'Show 15 Days'
    showDates = true
  } else {
    currentSearch.showFifteenDates(chart)
    e.target.innerText = 'Show Until Today'
    showDates = false
  }
}

const toggleDeaths = (e) => {
  let legend = document.querySelector('.c3-legend-item').textContent
  if (legend == 'deaths') {
    currentSearch.showCases(showDates)
    e.target.innerText = 'Show Deaths'
  } else {
    currentSearch.showDeaths(showDates)
    e.target.innerText = 'Show Cases'
  }
}

async function processForm(e) {
  e.preventDefault()
  const location = document.querySelector('#search-input').value
  const date = document.querySelector('#date').value

  // TODO: Add if statement to check value.
  document.querySelector('#loader').classList.remove('d-none')
  

  try {
  const searchInstance = await Search.create(location, date)
  currentSearch = searchInstance
  } catch (e) {
    console.log(e)
  }

  chart = currentSearch.generateChart('#cases-chart')
  document.querySelector('#show-btn').classList.remove('d-none')
  document.querySelector('#loader').classList.add('d-none')
}

document.querySelector('#search-form').addEventListener("submit", processForm)

document.querySelector('#show-btn').addEventListener('click', (e) => toggleAllDates(e))

document.querySelector('#death-btn').addEventListener('click', (e) => toggleDeaths(e))

// Method to add spinner loader.



