import { ref, computed, defineComponent, useRoute } from '@nuxtjs/composition-api'

function usePost () {
  const post = ref({})

  const fetchPost = async (id: number) => {
    fetch('https://jsonplaceholder.typicodcom/posts/' + id)
      .then(response => response.json())
      .then(json => post.value = json)
  }

  return {
    post,
    fetchPost
  }
}
