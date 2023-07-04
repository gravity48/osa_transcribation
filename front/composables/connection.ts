import {
  useContext,
  ssrRef,
  useAsync,
  useFetch,
  ref,
  computed,
  defineComponent,
  useRoute,
  watch, useStore
} from '@nuxtjs/composition-api';
import {Connections} from "~/types/types";

export const useConnection = () => {
  const {$axios} = useContext();
  const connection = ssrRef<Connections | Object>({});

  const fetchConnection = async (pk: string) => {
    return $axios.get(`api/v1/connections/connections/${pk}/`).then(r => r.data);
  }

  const watcherConnection = (newConn: Connections | Object, oldConn: Connections | Object) => {
    if ('id' in newConn && 'id' in oldConn) {
      if (newConn.id === oldConn.id) {
        console.log(newConn.db_system);
        debugger
        $axios.put(`api/v1/connections/connections/${newConn.id}/`, newConn).catch(error=>{
          console.log(error);
        });
      }
    }
  }


  // watch(connection, (newId, oldId, onCleanup)=>{
  //     debugger
  //     console.log('change')
  //   },
  //   {deep: true}
  // );
  //
  //

  // const fetchConnection = async () => {
  //   $axios.get(`api/v1/connections/connections/${route.value.params.id}/`)
  //     .then(response => connection.value = response.data)
  // }
  //
  // useAsync(
  //   fetchConnection
  // )

  return {
    connection,
    fetchConnection,
    watcherConnection,
  }
}
