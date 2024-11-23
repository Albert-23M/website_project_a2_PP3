<template>
    <div id="main-page" class="main-page" :class="view" v-if="searchResults && searchResults[0].list">
        <div class="col"  style="padding: var(--panel-gap)" v-for="(column, index) in searchResults" :key="index">
          <div class="header-content">
            <div class="title-wrap">
              <h3 class="main-page-title" v-if="column.title">
                {{ column.title }}
              </h3>
            </div>
          </div>

          <!-- Show the loader animation if its reading the books -->
          <div v-if="isLoading">
              <Transition name="slide-fade" mode="out-in">
                <component :is="view + '-holder'" :items="21"/>
              </Transition>
          </div>

          <!-- Types of view -->
          <Transition name="slide-fade" mode="out-in">
            <component :is="view" :column="column.list"/>
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
