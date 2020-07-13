// global currentSearch variable
const loader = document.querySelector('#loader')
const toggleBtn = document.querySelector('#toggle-btn')
const dateBtn = document.querySelector('#date-btn')
const deleteBtn = document.querySelector('#delete-btn')
const changeBtn = document.querySelector('#change-btn')
const message = document.querySelector('#message')
const searchHeader = document.querySelector('#search-heading')
const searchSubtitle = document.querySelector('#search-subtitle')
const casesChart = document.querySelector('#cases-chart')

let savedSearch = null
let chart = null
let showLoader = false
let showDates = false

async function loadSearch(id) {

  // Hide everything bui loader
  hide([casesChart, toggleBtn, dateBtn, deleteBtn, searchHeader, searchSubtitle, changeBtn])
  loader.classList.remove('d-none')

  try {
    const response = await Search.load(id)
    savedSearch = response

    // Render chart from results and show buttons and title
    chart = savedSearch.generateChart('#cases-chart')
    show([casesChart, toggleBtn, dateBtn, deleteBtn, searchHeader, searchSubtitle, changeBtn])

    deleteBtn.disabled = false
    searchHeader.innerText = `${savedSearch.location}`
    searchSubtitle.innerText = `(created at: ${savedSearch.createdAt})`
  
    // Hide and update error divs and buttons.
    hide([message, loader])
    message.innerText = ''
  
    } catch (err) {
      loader.classList.add('d-none')
      message.classList.remove('d-none')
      message.innerText = "Can't load search."
    }
}

// Toggle between showing 15 days from search date or all days until search creation
const toggleAllDates = (e) => {
  if (!showDates) {
    savedSearch.showAllDates(chart)
    e.target.innerText = '15 days'
    showDates = true
  } else {
    savedSearch.showFifteenDates(chart)
    e.target.innerText = 'To search date'
    showDates = false
  }
}

// Toggle between showing deaths and showing cases 
const toggleDeaths = (e) => {
  let legend = document.querySelector('.c3-legend-item').textContent
  if (legend == 'deaths') {
    savedSearch.showCases(showDates, chart)
    e.target.innerText = 'Show deaths'
  } else {
    savedSearch.showDeaths(showDates, chart)
    e.target.innerText = 'Show cases'
  }
}

// Delete search
async function deleteSearch(e) {
  e.preventDefault()
  try { 
    response = await savedSearch.delete()
    if (response === 'deleted') {
      message.innerText="Search deleted."
      message.classList.remove('d-none')
      deleteBtn.disabled = true
    } else {
      message.innerText="Can't delete search right now."
      message.classList.remove('d-none')
    }
  } catch (err) {
    message.innerText="Can't delete search."
  }
}

const showChange = () => {
  chart.toggle('change')
  changeBtn.innerText = (changeBtn.innerText === 'Show change') ? 'Hide change' : 'Show change'
}

const show = (btns) => btns.forEach(btn => btn.classList.remove('d-none'))
const hide = (btns) => btns.forEach(btn => btn.classList.add('d-none'))

const savedSearches = document.querySelectorAll('.overlay')
savedSearches.forEach((card) => card.addEventListener('click', loadSearch))

dateBtn.addEventListener('click', (e) => toggleAllDates(e))
toggleBtn.addEventListener('click', (e) => toggleDeaths(e))
deleteBtn.addEventListener('click', deleteSearch)
changeBtn.addEventListener('click', showChange)


