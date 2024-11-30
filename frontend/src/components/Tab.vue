<template>
    <div id="main-page" class="main-page" :class="view" v-if="searchResults && searchResults[0].list">
        <div class="col"  style="padding: var(--panel-gap)" v-for="(column, index) in searchResults" :key="index">
          <div class="header-content" v-show="column.list.length > 0">
            <div class="title-wrap">
              <h3 class="main-page-title" v-if="column.title">
                {{ column.title }}
              </h3>
            </div>
            <div class="title-wrap" v-if="column.list.length > maxItems">
              <router-link class="link-content" :to="showAll(column.title)">Show all</router-link>
            </div>
          </div>

          <!-- Show the loader animation if its reading the books -->
          <div v-if="isLoading">
              <Transition name="slide-fade" mode="out-in">
                <component :is="view + '-holder'" :items="maxItems"/>
              </Transition>
          </div>

          <!-- Types of view -->
          <Transition name="slide-fade" mode="out-in">
            <component :is="view" :column="getVisibleItems(column.list)"/>
          </Transition>

        </div>
    </div>
</template>

<script>
import GridTab from '@/components/GridTab'
import ListTab from '@/components/ListTab'
import CompactTab from '@/components/CompactTab'
import GridPlaceHolder from '@/components/GridPlaceHolder'
import ListPlaceHolder from '@/components/ListPlaceHolder'
import CompactPlaceHolder from '@/components/CompactPlaceHolder'

export default {
  name: 'DefaultTab',
  props: {
    searchResults: Array,
    loading: Boolean
  },
  data () {
    return {
      maxItems: 0,
      containerWidth: 0
    }
  },
  components: {
    'grid': GridTab,
    'list': ListTab,
    'compact': CompactTab,
    'grid-holder': GridPlaceHolder,
    'list-holder': ListPlaceHolder,
    'compact-holder': CompactPlaceHolder
  },
  computed: {
    view () {
      return this.$store.getters.displayMode
    },
    isLoading () {
      return this.loading
    }
  },
  methods: {
    calculateMaxItems () {
      const container = document.getElementById('main-page')
      if (container) {
        this.containerWidth = container.clientWidth

        const itemWidth = 10 * 16
        this.maxItems = Math.max(Math.floor(this.containerWidth / itemWidth) - 1, 1)
      }
    },

    getVisibleItems (list) {
      return list.slice(0, this.maxItems)
    },

    showAll (title) {
      const newQuery = {
        category: title,
        type: 'books'
      }
      const queryString = new URLSearchParams(newQuery).toString()
      return `${this.$route.path}?${queryString}`
    }
  },
  mounted () {
    this.calculateMaxItems()
    window.addEventListener('resize', this.calculateMaxItems)
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.calculateMaxItems)
  }
}
</script>

<style scoped>
/* Tab design */
.main-page{
  grid-area: main-page;
  padding-inline: calc(var(--panel-gap)*2 + var(--panel-gap)/2);
}

.main-page-title{
  font-weight: 600;
  font-size: var(--font-size-title);
}

.header-content{
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.link-content{
  padding-right: var(--panel-gap);
  cursor: pointer;
  color: var(--text-color);
  font-size: var(--font-size-xs);
  font-weight: 600;
}

.title-wrap{
  justify-content: end;
}

.slide-fade-enter-active, .slide-fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.slide-fade-enter, .slide-fade-leave-to {
  opacity: 0;
  transform: translateX(10px);
}
</style>
