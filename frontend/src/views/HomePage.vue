<template>
  <div>
    <div @resize="ResetColumnSizes">
      <div id="page" class="grid-layout min-vh-100">

        <main-header
                      :actualPage="currentTab"
                      @category-selected="startCategory"
                      @home-update="startHome"
                      @search-selected="startSearch"/>

        <library />

        <div id="leftdragbar" class="leftdragbar" @mousedown="StartLeftDrag"
                                                  @touchstart="StartLeftDrag"></div>

        <div id="tabs" class="tabs">
          <filter-header :searchResults="searchResults" :currentTab="currentTab" @genres-updated="handleGenresUpdate"/>

          <transition name="slide-fade" mode="out-in">
            <component :is="currentTab" :searchResults="searchResults" :loading="loading"/>
          </transition>

          <footer-tabs/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DefaultLibrary from '@/components/DefaultLibrary'
import BookPage from '@/components/BookPage'
import DefaultTab from '@/components/Tab'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import FilterHeader from '@/components/FilterHeader'
import CategoryTab from '@/components/CategoryTab'
import BookService from '../services/BookService'

const PageEnum = Object.freeze({
  HOME: 'default',
  SEARCH: 'book-page',
  CATEGORY: 'category',
  PROFILE: 'Profile'
})

export default {
  name: 'HomePage',
  components: {
    'main-header': Navbar,
    'library': DefaultLibrary,
    'default': DefaultTab,
    'book-page': BookPage,
    'footer-tabs': Footer,
    'filter-header': FilterHeader,
    'category': CategoryTab
  },

  data () {
    return {
      isLeftDragging: false,
      columnSizes: ['6rem', 'var(--dragbar-width)', 'auto'],
      searchResults: null,
      currentTab: PageEnum.HOME,
      loading: true
    }
  },
  created () {
    this.initializeSearchResults()
  },
  methods: {
    handleGenresUpdate (selectedGenres) {
      this.loading = true
      this.searchResults[0].list = []
      if (selectedGenres.length === 0) {
        this.initializeSearchResults()
        this.loading = false
        return
      }
      BookService.filterBooks(selectedGenres).then(response => {
        const books = response.data.data
        this.searchResults[0].list = books.map(book => ({
          type: 'book',
          data: {
            title: book.title,
            genres: book.genres || [],
            image: book.image,
            authors: book.authors || 'Unknown Author',
            synopsis: book.synopsis || 'No synopsis available',
            id: book.id_book
          }
        }))
        this.loading = false
      })
        .catch(error => {
          console.error('Error loading books:', error)
          this.loading = false
        })
    },
    ResetColumnSizes () {
      let page = document.getElementById('page')
      if (!page) return

      const [leftCol, dragbar, mainContent] = this.columnSizes
      const totalWidth = leftCol + dragbar + mainContent
      this.columnSizes = [
        `${(leftCol / totalWidth) * 100}fr`,
        `8px`,
        `${(mainContent / totalWidth) * 100}fr`
      ]
      page.style.gridTemplateColumns = this.columnSizes.join(' ')
    },
    SetCursor (cursor) {
      let page = document.getElementById('page')
      page.style.cursor = cursor
    },
    StartLeftDrag (event) {
      this.isLeftDragging = true
      this.SetCursor('ew-resize')
      window.addEventListener('mousemove', this.OnDrag)
      window.addEventListener('mouseup', this.EndDrag)
      window.addEventListener('touchmove', this.OnDrag, { passive: false })
      window.addEventListener('touchend', this.EndDrag, { passive: false })
      event.preventDefault()
    },
    EndDrag () {
      this.isLeftDragging = false
      this.SetCursor('auto')
      window.removeEventListener('mousemove', this.OnDrag)
      window.removeEventListener('mouseup', this.EndDrag)
      window.removeEventListener('touchmove', this.OnDrag)
      window.removeEventListener('touchend', this.EndDrag)
    },
    OnDrag (event) {
      let page = document.getElementById('page')
      let mousePosX = event.clientX || (event.touches && event.touches[0] ? event.touches[0].clientX : 0)
      if (this.isLeftDragging && mousePosX < (page.clientWidth / 2) && mousePosX > 114) {
        let gap = parseFloat(window.getComputedStyle(page).gap)
        let padding = parseFloat(window.getComputedStyle(page).paddingRight)

        let leftColWidth = mousePosX - gap / 2 - gap - padding

        this.columnSizes = [
          Math.max(leftColWidth, 0),
          gap,
          Math.max(page.clientWidth - mousePosX - gap / 2 - gap - padding, 0)
        ]

        page.style.gridTemplateColumns = this.columnSizes.map(c => c + 'px').join(' ')

        event.preventDefault()
      }
    },
    startSearch (data) {
      this.currentTab = PageEnum.SEARCH
      console.log('Searching for:', data)

      // If a request is made to the API, it should be async
      // Book example
      if (data[1] === 'book') {
        this.searchResults = [
          {
            title: 'Search',
            list:
              {
                type: 'book',
                data: {
                  title: 'Book1',
                  Authors: 'AuthorsName',
                  Synopsis: 'Synopsis info',
                  BuyLink: 'BuyLink info',
                  Genres: 'Gerne1, Gernre2',
                  Rating: 0.0,
                  Editorial: 'EditorialName',
                  Comments: [],
                  PublicationDate: '11/11/11',
                  Image: 'image'
                }
              }
          }
        ]
      } else if (data[1] === 'user') {
        //  User example
        this.searchResults = [
          {
            title: 'Search',
            list:
              {
                type: 'user',
                data: {
                  name: 'Book1',
                  surname: 'AuthorsName',
                  username: 'Synopsis info',
                  email: 'BuyLink info'
                }
              }
          }
        ]
      }
    },
    startHome () {
      this.currentTab = PageEnum.HOME
      this.initializeSearchResults()
    },
    async initializeSearchResults () {
      this.loading = true
      const newSearchResults = [
        {
          title: 'Popular Books',
          list: []
        },
        {
          title: 'Recently Read',
          list: []
        },
        {
          title: 'Followed Users',
          list: []
        }
      ]
      BookService.readBooks().then(response => {
        const books = response.data.data
        newSearchResults[0].list = books.map(book => ({
          type: 'book',
          data: {
            title: book.title,
            genres: book.genres || [],
            image: book.image,
            authors: book.authors || 'Unknown Author',
            synopsis: book.synopsis || 'No synopsis available',
            id: book.id_book
          }
        }))
        this.loading = false
      })
        .catch(error => {
          console.error('Error loading books:', error)
          this.loading = false
        })
      if (this.searchResults !== newSearchResults) {
        this.searchResults = newSearchResults
      }
    },
    startCategory (data) {
      if (this.currentTab !== PageEnum.CATEGORY) {
        if (this.searchResults.length === 1) {
          this.initializeSearchResults()
        }
        this.currentTab = PageEnum.CATEGORY
        const newSearch = this.searchResults.find(column => column.title === data[0])
        if (newSearch) {
          this.searchResults = [newSearch]
        }
      }
    }
  },
  computed: {
    username () {
      return this.$store.getters.username
    }
  },
  mounted () {
    window.addEventListener('resize', this.ResetColumnSizes)
  },
  beforeUnmount () {
    window.removeEventListener('resize', this.ResetColumnSizes)
  }
}
</script>

<style scoped>
.grid-layout {
  display: grid;
  gap: var(--panel-gap);
  grid-template-areas: 'global-nav global-nav global-nav'
                       'left-slider leftdragbar tabs';
  grid-template-rows: auto 1fr;
  grid-template-columns: 6rem var(--dragbar-width) auto;
  padding: var(--panel-gap);
  padding-top: 0;
  background-color: var(--main-background);
}

.leftdragbar {
  grid-area: leftdragbar;
  cursor: ew-resize;
  transition: transform 0.3s ease-in-out;
}

.leftdragbar:hover{
  background: var(--hover-dragbar-color);
}

.tabs {
  background: var(--box-background-color);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: calc(var(--border-radius) * 2);
  overflow: auto;
  grid-area: tabs;
  margin-left: calc(-1 * var(--panel-gap));
  display: grid;
  gap: var(--panel-gap);
  grid-template-areas: 'filter-option'
                       'main-page'
                       'footer';
  grid-template-rows: auto 1fr auto;
  max-height: 100vh;
  color: var(--text-color);
}

.slide-fade-enter-active, .slide-fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.slide-fade-enter, .slide-fade-leave-to {
  opacity: 0;
  transform: translateX(10px);
}

@media(max-width: 42.375rem){
  .grid-layout{
    grid-template-areas: 'global-nav global-nav global-nav'
                         'left-slider left-slider left-slider'
                         'leftdragbar leftdragbar leftdragbar'
                         'tabs tabs tabs';
    grid-template-rows: 5rem 6rem 0rem auto;
    grid-template-columns: auto;
  }

  .tabs{
    margin: var(--panel-gap);
  }
}
</style>
