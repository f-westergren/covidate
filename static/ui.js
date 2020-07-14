// global currentSearch variable
const loader = document.querySelector('#loader')
const toggleBtn = document.querySelector('#toggle-btn')
const dateBtn = document.querySelector('#date-btn')
const saveBtn = document.querySelector('#save-btn')
const changeBtn = document.querySelector('#change-btn')
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
    e.target.innerText = '15 days'
    showDates = true
  } else {
    currentSearch.showFifteenDates(chart)
    e.target.innerText = 'Today'
    showDates = false
  }
}

// Toggle between showing deaths and showing cases 
const toggleDeaths = (e) => {
  let legend = document.querySelector('.c3-legend-item').textContent
  
  if (legend == 'deaths') {
    currentSearch.showCases(showDates, chart)
    e.target.innerText = 'Deaths'
  } else {
    currentSearch.showDeaths(showDates, chart)
    e.target.innerText = 'Cases'
  }
}

const show = (btns) => btns.forEach(btn => btn.classList.remove('d-none'))
const hide = (btns) => btns.forEach(btn => btn.classList.add('d-none'))

const showChange = () => {
  chart.toggle('change')
  changeBtn.innerText = (changeBtn.innerText === 'Show change') ? 'Hide change' : 'Show change'
}

async function processForm(e) {
  e.preventDefault()
  const location = document.querySelector('#search-input').value
  const date = document.querySelector('#date').value

  show([loader])

  try {
  const response = await Search.create(location, date)
  currentSearch = response

  // Render chart from results
  chart = currentSearch.generateChart('#cases-chart')

  // Show buttons
  show([toggleBtn, dateBtn, saveBtn, changeBtn])
  dateBtn.innerText='Today'
  changeBtn.innerText='Show change'

  // Hide and update error divs and buttons.
  hide([saveError, searchError, loader])
  saveBtn.innerText = 'Save search'
  saveBtn.disabled = false

  } catch (err) {
    hide([loader])
    show([searchError])
    if (err.response == 400) {
    searchError.innerText = err.response.data
    } else {
      console.log(err)
    }
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
      show([searchError])
      saveError.innerText = "Can't save search right now."
    }

    // Hide description input field
    hide([descriptionDiv, descriptionMsg])
    description.innerText = ''

  } else {

  // Show description input field
  showDescription = true
  show([descriptionDiv, descriptionMsg])

  }
}

document.querySelector('#search-form').addEventListener('submit', processForm)
dateBtn.addEventListener('click', toggleAllDates)
toggleBtn.addEventListener('click', toggleDeaths)
saveBtn.addEventListener('click', saveSearch)
document.querySelector('#change-btn').addEventListener('click', showChange)