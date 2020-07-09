// global currentSearch variable
const loader = document.querySelector('#loader')
const toggleBtn = document.querySelector('#toggle-btn')
const dateBtn = document.querySelector('#date-btn')
const saveBtn = document.querySelector('#save-btn')
const saveError = document.querySelector('#save-error')
const searchError = document.querySelector('#search-error')
const descriptionDiv = document.querySelector('#description-div')
const descriptionMsg = document.querySelector('#description-msg')

let currentSearch = null
let chart = null
let showLoader = false
let showDates = false
let showDescription = false
let description = undefined

// Toggle between showing 15 days from search date or all days until search creation
const toggleAllDates = (e) => {
  if (!showDates) {
    currentSearch.showAllDates(chart)
    e.target.innerText = 'Show 15 days'
    showDates = true
  } else {
    currentSearch.showFifteenDates(chart)
    e.target.innerText = 'Show until today'
    showDates = false
  }
}

// Toggle between showing deaths and showing cases 
const toggleDeaths = (e) => {
  let legend = document.querySelector('.c3-legend-item').textContent

  if (legend == 'deaths') {
    currentSearch.showCases(showDates)
    e.target.innerText = 'Show deaths'
  } else {
    currentSearch.showDeaths(showDates)
    e.target.innerText = 'Show cases'
  }
}

async function processForm(e) {
  e.preventDefault()
  const location = document.querySelector('#search-input').value
  const date = document.querySelector('#date').value

  document.querySelector('#loader').classList.remove('d-none')

  try {
  const response = await Search.create(location, date)
  currentSearch = response

  // Render chart from results
  chart = currentSearch.generateChart('#cases-chart')

  // Show buttons
  toggleBtn.classList.remove('d-none')
  dateBtn.classList.remove('d-none')
  dateBtn.innerText='Show until today'
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

  // If description input field is showing
  if (showDescription) {

    // Get value from description input
    let description = document.querySelector('#description').value

    try {
      const response = await currentSearch.save(description)
      if (response.data === 'saved') {
        saveBtn.innerText = 'Saved'
        saveBtn.disabled = true

        // Deactivate description input field
        showDescription = false
      } else if (response.data === 'login') {
        window.location.href = '/login?saveSearch=true'
      }
    } catch (e) {
      saveError.classList.remove('d-none')
      saveError.innerText = "Can't save search right now."
    }

    // Hide description input field
    descriptionDiv.classList.add('d-none')
    descriptionMsg.classList.add('d-none')
    description.innerText = ''

  } else {

  // Show description input field
  showDescription = true
  descriptionDiv.classList.remove('d-none')
  descriptionMsg.classList.remove('d-none')
  }
}

document.querySelector('#search-form').addEventListener('submit', processForm)
dateBtn.addEventListener('click', toggleAllDates)
toggleBtn.addEventListener('click', toggleDeaths)
saveBtn.addEventListener('click', saveSearch)