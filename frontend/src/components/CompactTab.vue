<template>
  <div class="options-content" v-show="column.length > 0">

    <div class="header-compact">
      <div class="left">
        Book's name
      </div>
      <div class="right">
        Author's name
      </div>
    </div>

    <div class="line"/>

    <router-link v-for="(item, index) in column" :key="index" v-if="item.data" class="btn card-book-wrap" :to="startSearch(item)">
          <h5 class="book-name left">
            {{ item.data.title }}
          </h5>
          <h4 class="author-name right">
            {{ item.data.authors }}
          </h4>
    </router-link>

  </div>
</template>

<script>
export default {
  name: 'CompactTab',
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
    }
  }
}
</script>

<style scoped>

.options-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn {
  border: 0;
  padding: var(--panel-gap);
  border-radius: var(--border-radius);
  color: var(--text-color);

}

.btn:hover {
  background: var(--half-transparent-background);
}

.header-compact, .card-book-wrap{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--panel-gap);
}

.left {
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  margin-right: 1rem;
}

.right {
  text-align: right;
}

.line {
  height: 1px;
  background: var(--gray-background);
  box-sizing: border-box;
  margin-top: calc(var(--panel-gap) * -1);
  margin-inline: var(--panel-gap);
}

.book-name{
    text-transform: uppercase;
}

.book-name, .author-name{
  font-size: var(--font-size-xs);
  font-weight: 600;
}

</style>
