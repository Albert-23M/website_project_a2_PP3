<template>
  <nav id="header" class="header">
    <!-- Logo image -->
    <div class="left-wrap">
      <div class="image-wrap">
         <img loading="lazy"  src="@/assets/bookhub-white.svg" alt="BookHub Logo" style="height: 3rem">
      </div>
    </div>

    <!-- Home and SearchBar -->
    <div  class="center-wrap">
      <div class="home-search-wrap">
        <div class="tooltip-container">
          <span class="tooltip-text">Home</span>
          <router-link to="/" class="btn home-icon" custom>
              <svg width="43" height="47" viewBox="0 0 43 47" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 16.4088L21.25 1.01349L41.5 16.4088V40.6013C41.5 41.7679 41.3803 43.5467 40.5363
                44.3716C40.5363 45.6284 29.1935 45 28 45V28.0338H14.5V45C13.3065 45 1.96491 45.6284 1.96491
                44.3716C1.121 43.5467 1 41.7679 1 40.6013V16.4088Z"
                      :fill="actualPage==='default'? 'white' : 'transparent'" stroke="white" stroke-width="4"
                      stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
          </router-link>
          </div>

        <!-- Miss SearchBar Here -->
        <span class="form-search">
          <div class="search-wrap">
            <form role="search" class="search" @submit.prevent>

              <div class="search-icon-wrap">
                <div class="tooltip-container" style="padding-inline: var(--panel-gap);">
                  <span class="tooltip-text">Search</span>
                  <svg style="display: block; padding-inline: var(--panel-gap)" width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M38 38L29.3 29.3M34 18C34 26.8366 26.8366 34 18 34C9.16344 34 2 26.8366 2 18C2 9.16344 9.16344 2 18 2C26.8366 2 34 9.16344 34 18Z" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>

              <div class="input-group-wrap" ref="input-group-wrap" @click="toggleSuggestions">
                <input class="input-search" :class="{active: isLoading}" type="search" spellcheck="false" placeholder="Search something"
                       value="" tabindex="0" maxlength="200" v-model="textInput">

                <!-- Suggestions -->
                <suggestions :filteredSuggestionsUsers="filteredSuggestionsUsers"
                              :filteredSuggestionsBooks="filteredSuggestionsBooks"
                             :errorMessages="errorMessages"
                             v-show="getShowSuggestions"
                             />
              </div>

              <div class="genre-line-wrap">
                 <div class="tooltip-container">
                   <span class="tooltip-text">Genres</span>
                   <div class="genre-icon">

                      <svg width="10" height="30">
                        <line x1="5" y1="0" x2="5" y2="100%" stroke="white" stroke-width="2" />
                      </svg>

                      <svg style="padding-inline: var(--panel-gap)" width="40"
                           height="40" viewBox="0 0 44 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M22 10C22 7.87827 21.1571 5.84344 19.6569 4.34315C18.1566 2.84285 16.1217 2 14
                        2H2V32H16C17.5913 32 19.1174 32.6321 20.2426 33.7574C21.3679 34.8826 22 36.4087 22
                        38M22 10V38M22 10C22 7.87827 22.8429 5.84344 24.3431 4.34315C25.8434 2.84285 27.8783 2 30
                        2H42V32H28C26.4087 32 24.8826 32.6321 23.7574 33.7574C22.6321 34.8826 22 36.4087 22 38"
                              :fill="actualPage ==='book-page'? 'white' : 'transparent'"
                              stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </div>
                 </div>
              </div>
            </form>
          </div>
        </span>

        </div>
    </div>

      <div class="right-wrap" v-if="username !== ''">
          <div class="tooltip-container">
            <span class="tooltip-text">Help</span>
            <div class="btn help-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18.18 18C18.6502 16.6633 19.5783 15.5362 20.7999 14.8183C22.0215 14.1003 23.4578 13.8379
              24.8544 14.0774C26.2509 14.317 27.5176 15.043 28.4302 16.1271C29.3427 17.2111 29.8421 18.583 29.84
              20C29.84 24 23.84 26 23.84 26M24 34H24.02"
                    stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        <div class="tooltip-container">
            <span class="tooltip-text">Profile</span>
            <div class="btn profile-icon">
              <img loading="lazy" src="@/assets/user-black.svg" alt="Profile Picture" style="height: 75%">
            </div>
          </div>
      </div>
      <div class="right-wrap" v-else>
        <router-link to="/signup" v-slot="{ navigate }" custom>
          <button @click="navigate" class="btn btn-signup">Sign up</button>
        </router-link>
        <router-link to="/login" v-slot="{ navigate }" custom>
          <button @click="navigate" class="btn btn-login">Login</button>
        </router-link>
      </div>
  </nav>
</template>

<script>
import Suggestions from '@/components/Suggestions'
import BookService from '../services/BookService'
import debounce from 'lodash/debounce'
import UserService from '../services/UserService'

const PageEnum = Object.freeze({
  HOME: 'default',
  SEARCH: 'book-page',
  CATEGORY: 'category',
  PROFILE: 'Profile'
})

const CategoryEnum = Object.freeze({
  POPULAR: 'Popular Books',
  RECENTLY_READ: 'Recently Read',
  FOLLOWED: 'Followed Users'
})

export default {
  name: 'Navbar',
  components: {'suggestions': Suggestions},
  props: {
    actualPage: PageEnum
  },
  data () {
    return {
      textInput: '',
      type: '',
      id: '',
      suggestions: [],
      filteredSuggestionsUsers: [],
      filteredSuggestionsBooks: [],
      errorMessages: [],
      showSuggestions: false,
      isLoading: false
    }
  },
  created () {
    this.debouncedFilter = debounce(this.filterSuggestions, 300)
  },
  watch: {
    '$route.query': {
      handler () {
        this.textInput = this.$route.query.search || ''
        this.type = this.$route.query.type || ''
        this.id = this.$route.query.id || ''
        const categorySearch = this.$route.query.category || ''
        if (this.textInput !== '' && this.type !== '' && this.id !== '') {
          this.startSearch()
        } else if (categorySearch !== '' && this.type !== '') {
          this.setCategory(categorySearch)
        } else {
          this.setPageHome()
          this.filteredSuggestionsUsers = []
          this.filteredSuggestionsBooks = []
        }
      },
      immediate: true
    },
    textInput () {
      this.debouncedFilter()
    }
  },
  computed: {
    username () {
      return this.$store.getters.username
    },
    getShowSuggestions () {
      return this.showSuggestions
    }
  },
  methods: {
    toggleSuggestions () {
      this.showSuggestions = true
    },
    setPageHome () {
      if (this.actualPage !== PageEnum.HOME) {
        this.filteredSuggestionsUsers = []
        this.filteredSuggestionsBooks = []
        this.$emit('home-update')

        this.clearRoute()
      }
    },
    setPageSearch () {
      if (this.actualPage !== PageEnum.SEARCH) {
        this.$emit('search-selected', [this.textInput, this.type])
      }
    },
    setCategory (categorySearch) {
      if ((categorySearch === CategoryEnum.POPULAR || categorySearch === CategoryEnum.FOLLOWED ||
        categorySearch === CategoryEnum.RECENTLY_READ) && this.actualPage !== PageEnum.CATEGORY) {
        this.$emit('category-selected', [categorySearch, this.type])
      } else if (this.actualPage !== PageEnum.CATEGORY) {
        this.$router.push('/not-found')
      }
    },
    clearRoute () {
      this.textInput = ''
      if ((this.$route.query.search || this.$route.query.category) && this.$route.query.type) {
        this.$router.replace({query: {}}).catch(() => {
          console.error('The router url is the same')
        })
      }
    },
    async filterSuggestions () {
      this.isLoading = true
      this.errorMessages = []
      this.filteredSuggestionsUsers = []
      this.filteredSuggestionsBooks = []
      if (this.textInput.trim()) {
        if (this.$route.query.search &&
          this.$route.query.type &&
          this.textInput === this.$route.query.search &&
          this.$route.query.type === this.type) {
          this.filteredSuggestionsUsers = []
          this.filteredSuggestionsBooks = []
          this.isLoading = false
          return
        }

        if (this.hasSpecialCharacters(this.textInput.trim())) {
          this.errorMessages.push({name: 'No special characters allowed', type: 'error'})
          this.filteredSuggestionsUsers = []
          this.filteredSuggestionsBooks = []
          return
        }
        const input = this.textInput.trim().toLowerCase()
        Promise.all([
          UserService.readTop5MatchedUsers(input)
            .then(response => {
              const users = response.data.data
              this.filteredSuggestionsUsers = users.map(user => ({
                type: 'user',
                id: user.id_user,
                name: user.name + ' ' + user.surname
              }))
              this.isLoading = false
            })
            .catch(error => {
              console.error('Error loading users:', error)
              this.filteredSuggestionsUsers = []
              this.isLoading = false
            }),
          BookService.readTop5MatchedBooks(input)
            .then(response => {
              const books = response.data.data
              this.filteredSuggestionsBooks = books.map(book => ({
                type: 'book',
                id: book.id_book,
                name: book.title
              }))
              this.isLoading = false
            })
            .catch(error => {
              console.error('Error loading books:', error)
              this.filteredSuggestionsBooks = []
              this.isLoading = false
            })
        ])
          .then(() => {
            if (!this.filteredSuggestionsUsers.length && !this.filteredSuggestionsBooks.length) {
              this.errorMessages = []
              this.errorMessages.push({name: 'No match found', type: 'error'})
            }
          })
      } else {
        this.filteredSuggestionsUsers = []
        this.filteredSuggestionsBooks = []
        this.isLoading = false
      }
    },
    async startSearch () {
      this.filteredSuggestionsUsers = []
      this.filteredSuggestionsBooks = []

      if (this.type === 'book') {
        BookService.readBookById(this.id).then(response => {
          const book = response.data
          if (book.title !== this.textInput) {
            this.$router.push('/not-found')
          }
        }).catch(error => {
          console.error('Error reading a book:', error)
          this.$router.push('/not-found')
        })
      } else if (this.type === 'user') {
        UserService.readUserById(this.id).then(response => {
          const user = response.data
          if (user.name + ' ' + user.surname !== this.textInput) {
            this.$router.push('/not-found')
          }
        }).catch(error => {
          console.error('Error reading a book:', error)
          this.$router.push('/not-found')
        })
      }

      if (this.textInput.trim() !== '') {
        this.setPageSearch()
      }
    },
    hasSpecialCharacters (input) {
      const specialCharactersRegex = /^[a-zA-ZñÑáéíóúÁÉÍÓÚüçÜ0-9]+( +[a-zA-ZñÑáéíóúÁÉÍÓÚüçÜ0-9]+)*$/
      return !specialCharactersRegex.test(input)
    },
    closeSuggestions (event) {
      const group = this.$refs['input-group-wrap']
      if (group && !group.contains(event.target)) {
        this.showSuggestions = false
      }
    }
  },
  mounted () {
    document.addEventListener('click', this.closeSuggestions)
  },
  beforeDestroy () {
    document.removeEventListener('click', this.closeSuggestions)
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: calc(4rem + var(--panel-gap)*2);
  padding: var(--panel-gap);
  position: relative;
  grid-area: global-nav;
}

.left-wrap{
  display: flex;
  align-items: center;
  flex-flow: row nowrap;
  gap: var(--panel-gap);
  z-index: 1;
}

.image-wrap{
  display: flex;
  flex-direction: row;
  margin: 17px;
  align-items: center;
}

.center-wrap{
  display: flex;
  margin: calc(var(--panel-gap)*-1);
  flex: 1;
  justify-content: center;
  align-items: center;
  gap: 0;
  z-index: 1;
}

.home-search-wrap{
  display: flex;
  align-items: center;
}

.help-icon, .profile-icon, .home-icon{
  display: flex;
  border-radius: 50%;
  background-color: var(--button-background);
  height: 3rem;
  width: 3rem;
  align-items: center;
  transition: transform 0.3s ease-in-out;
  margin-inline-start: var(--panel-gap);
  justify-content: center;
}

.help-icon.btn {
  padding: 0;
}

.right-wrap{
  display: flex;
  flex-flow: row nowrap;
  gap: var(--panel-gap);
  justify-content: end;
  align-items: center;
  z-index: 1;
}

.btn-signup, .btn-login{
  margin-right: var(--panel-gap);
  font-weight: 700;
  color: var(--text-color);
  width: 7rem;
  transition: transform 0.3s ease-in-out;
  border-radius: calc(var(--border-radius) * 2);
}
.btn-login{
  background: var(--purple-background);
}
.btn-signup:hover,
.help-icon:hover,
.home-icon:hover,
.profile-icon:hover,
.btn-login:hover {
  transform: scale(1.05);
}

.form-search{
  height: 100%;
  width: 100%;
  border: 0;
  margin: 0;
  padding: 0;
  vertical-align: baseline;
}

.search-wrap{
  padding-inline: var(--panel-gap);
  position: relative;
  width: 100%;
}

.search{
  position: relative;
  transition: all .22s ease-in;
  background: var(--button-background);
  border-radius: 500px;
  width: 100%;
}

.search-icon-wrap{
  display: flex;
  left: 0;
  right: auto;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.input-group-wrap{
  border: 0;
  margin: 0;
  padding: 0;
  vertical-align: baseline;
}

.input-search {
  padding-block: calc(var(--panel-gap) * 1.5);
  padding-right: calc(var(--panel-gap) * 9);
  background: transparent;
  border-radius: calc(var(--border-radius) * 100);
  cursor: pointer;
  padding-left: calc(var(--panel-gap) * 7);
  border: 0.125rem solid transparent;
  color: var(--text-color);
  outline: none;
}

.input-search.active{
  --border-angle: 0turn;
  --main-bg: conic-gradient(
    from var(--border-angle),
    var(--button-background),
    var(--button-background) 5%,
    var(--button-background) 60%,
    var(--button-background) 95%
  );
  --gradient-border: conic-gradient(
    from var(--border-angle),
    transparent 25%,
    var(--text-color),
    var(--purple-background) 99%,
    transparent
  );
  background: var(--main-bg) padding-box,
  var(--gradient-border) border-box,
  var(--main-bg) border-box;

  animation: bg-spin 3s linear infinite;
  transition: box-shadow 0.3s ease;
}

.input-search::-webkit-search-cancel-button {
  -webkit-appearance: none;
  appearance: none;
}

.input-search:focus {
  border-color: var(--text-color);
}

.input-search.active:focus {
  border-color: transparent;
}

.search:hover {
  background: var(--half-transparent-background);
  box-shadow: inset 0 0 0.25rem var(--search-color-shadow);
}

.genre-line-wrap{
  display: flex;
  align-items: center;
  position: absolute;
  vertical-align: baseline;
  top: 50%;
  left: calc(var(--panel-gap) * 30);
  transform: translateY(-50%);
}

@media (max-width: 45.625rem) {

  .home-icon{
    display: none;
  }

  .btn-signup{
    display: none;
  }

  .btn-login{
    width: 5rem;
    border-radius: calc(var(--border-radius)* 9);
    margin-left: var(--panel-gap);
  }
}

@keyframes bg-spin {
  to {
    --border-angle: 1turn;
  }
}

@property --border-angle {
  syntax: "<angle>";
  inherits: true;
  initial-value: 0turn;
}
</style>
