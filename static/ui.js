// global currentSearch variable
const loader = document.querySelector('#loader')
const toggleBtn = document.querySelector('#toggle-btn')
const dateBtn = document.querySelector('#date-btn')
const saveBtn = document.querySelector('#save-btn')
const saveError = document.querySelector('#save-error')
const searchError = document.querySelector('#search-error')

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
  const response = await Search.create(location, date)
  currentSearch = response
  
  // Render chart from results
  chart = currentSearch.generateChart('#cases-chart')

  // Show buttons
  toggleBtn.classList.remove('d-none')
  dateBtn.classList.remove('d-none')
  saveBtn.classList.remove('d-none')

  // Hide and update error divs and buttons.
  saveBtn.innerText = 'Save Search'
  saveBtn.disabled = false
  saveError.classList.add('d-none')
  searchError.classList.add('d-none')
  loader.classList.add('d-none')

  } catch (err) {
    loader.classList.add('d-none')
    searchError.classList.remove('d-none')
    searchError.innerText = err
  }
}

async function saveSearch(e) {
  e.preventDefault()
  try {
    const response = await currentSearch.save()
    if (response.data === 'saved') {
      saveBtn.innerTex = 'Saved'
      saveBtn.disabled = true
    } else if (response.data === 'login') {
      window.location.href = '/login?saveSearch=true'
    }
  } catch (e) {
    saveError.classList.remove('d-none')
    saveError.innerText = "Can't save search right now."
  }
}

document.querySelector('#search-form').addEventListener('submit', processForm)
dateBtn.addEventListener('click', toggleAllDates)
toggleBtn.addEventListener('click', toggleDeaths)
saveBtn.addEventListener('click', saveSearch)