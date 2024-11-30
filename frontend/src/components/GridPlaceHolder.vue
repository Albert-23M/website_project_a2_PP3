<template>
  <div class="options-content">
    <!-- Placeholder Content for Grid -->
    <div class="card-book-placeholder" v-for="index in items" :key="index">
      <div class="image-placeholder"></div>
      <div class="text-wrap">
        <div class="text-card-placeholder"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GridTabPlaceHolder',
  props: {
    items: Number
  }
}
</script>

<style scoped>
.options-content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
  gap: 1rem;
  align-items: center;
  padding-block: var(--panel-gap);
}

.card-book-placeholder {
  color: var(--text-color);
  display: flex;
  flex-direction: column;
  gap: var(--panel-gap);
  background: transparent;
  border-radius: var(--border-radius);
  padding: var(--panel-gap);
  align-items: center;
}

.image-placeholder {
  height: 15.5rem;
  width: 11rem;
  background: linear-gradient(to right, #eee 2%, #ddd 18%, #eee 33%);
  background-size: 200% 100%;
  animation: placeholderAnimate 3s infinite linear forwards;
  border-radius: var(--border-radius);
}

.text-wrap {
  justify-content: center;
  display: flex;
  width: 10rem;
}

.text-card-placeholder {
  width: 70%;
  height: 20px;
  background: linear-gradient(to right, #eee 2%, #ddd 18%, #eee 33%);
  background-size: 200% 100%;
  animation: placeholderAnimate 3s infinite linear;
  border-radius: var(--border-radius);
}

@keyframes placeholderAnimate {
  0% {
    background-position: -650px 0;
  }
  100% {
    background-position: 650px 0;
  }
}
</style>
