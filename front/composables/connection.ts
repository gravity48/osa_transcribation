import {
  useContext,
  ssrRef
} from '@nuxtjs/composition-api';
import {Connections} from "~/types/types";

let timeout:  ReturnType<typeof setTimeout>;

export const useConnection = () => {
  const {$axios} = useContext();
  const connection = ssrRef<Connections | Object>({
    options: {}
  });

  const fetchConnection = async (pk: string) => {
    return $axios.get(`api/v1/connections/connections/${pk}/`).then(r => r.data);
  }

  const watcherConnection = (newConn: Connections | Object, oldConn: Connections | Object) => {
    if ('id' in newConn && 'id' in oldConn) {
      if (newConn.id === oldConn.id) {
        clearTimeout(timeout)
        timeout = setTimeout( () => $axios.put(`api/v1/connections/connections/${newConn.id}/`, newConn).catch(error=>{
          console.log(error);
        }), 1000)

      }
    }
  }

  return {
    connection,
    fetchConnection,
    watcherConnection,
  }
}
