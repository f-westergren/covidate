// global currentSearch variable
const loader = document.querySelector('#loader')
const toggleBtn = document.querySelector('#toggle-btn')
const dateBtn = document.querySelector('#date-btn')
const saveBtn = document.querySelector('#save-btn')

let currentSearch = null
let chart = null
let showLoader = false
let showDates = false

// Toggle between showing 15 days from search date or all days until search creation
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

// Toggle between showing deaths and showing cases 
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
  toggleBtn.classList.remove('d-none')
  dateBtn.classList.remove('d-none')
  loader.classList.add('d-none')
}

document.querySelector('#search-form').addEventListener("submit", processForm)
dateBtn.addEventListener('click', (e) => toggleAllDates(e))
toggleBtn.addEventListener('click', (e) => toggleDeaths(e))
saveBtn.addEventListener('click', async function() {
  await currentSearch.save()
}
)