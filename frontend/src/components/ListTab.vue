<template>
  <div class="options-content">
        <router-link v-for="(item, index) in column" :key="index" v-if="item.data" class="btn" :to="startSearch(item)">
          <div class="card-book" >
            <div class="image-wrap">
              <img loading="lazy" :src="item.data.image" class="image" alt="Cover Book">
            </div>
            <div class="text-wrap">
              <div class="genres">
               <a v-for="genre in item.data.genres.split(',')" :key="genre" :style="{ color: getGenreColor(genre) }">
                  {{ genre }}
                </a>
              </div>
              <h4 class="text-card">
                {{ item.data.title }}
              </h4>
              <h5 class="author">
                By {{ item.data.authors }}
              </h5>
              <p class="synopsis">
                {{ item.data.synopsis }}
              </p>
            </div>
          </div>
        </router-link>
  </div>
</template>

<script>
import {genreColors} from '@/assets/genresColors'

export default {
  name: 'ListTab',
  props: {
    column: Array
  },
  methods: {
    startSearch (item) {
      const newQuery = {
        search: item.data.title,
        type: item.type,
        id: item.data.id
      }

      const queryString = new URLSearchParams(newQuery).toString()
      return `${this.$route.path}?${queryString}`
    },
    getGenreColor (genre) {
      return genreColors[genre.trim()] || '#d1cff8'
    }
  }
}
</script>
<style scoped>
.btn{
  border: 0;
}

.btn{
  padding: var(--panel-gap);
  border: 0;
  border-radius: var(--border-radius);
}

.btn:hover{
  background: var(--half-transparent-background);
}

.options-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card-book {
  display: flex;
  gap: var(--panel-gap);
  flex-direction: row;
  padding-bottom: var(--panel-gap);
}

.image-wrap{
  order: 1;
  width: 25%;
  align-content: center;
  align-items: center;
}

.image {
  height: 11rem;
  border-radius: var(--border-radius);
  box-shadow: 0 0 0.5rem var(--half-transparent-main-background);
}

.text-wrap{
  order: 2;
  padding: calc(var(--panel-gap));
  margin-left: calc(var(--panel-gap) *3);
  display: grid;
  grid-template-areas: 'genres'
                        'title'
                       'author'
                       'synopsis';
  grid-template-rows: 1fr 1fr 1fr auto;
  align-content: center;
  align-items: center;
  color: var(--text-color);
  width: 100%;
}

.genres{
  grid-area: genres;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  color: var(--second-text-color);
  line-height: 1rem;
  font-size: var(--font-size-xs);
  gap: var(--panel-gap);
  margin-bottom: calc(var(--panel-gap) /2);
  font-weight: 700;
}

.text-card{
  grid-area: title;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: var(--font-size-medium);
  font-weight: 700;
  text-align: left;
}

.author{
  grid-area: author;
  display: flex;
  font-style: italic;
  font-weight: 700;
  font-size: var(--font-size-xs);
}

.synopsis{
  grid-area: synopsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: var(--font-size-xs);
  text-align: left;
}
</style>
