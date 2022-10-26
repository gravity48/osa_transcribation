import api from "@/services/api";
import api_without_preloader from "@/services/api_without_preloader";

class ViewService{
    users_api(){
        return api.get('user/');
    }
    get_connections(){
        return api.get('connections/');
    }
    get_db_systems(){
        return api.get('database_system/');
    }
    add_connections(){
        return api.post('connections/')
    }
    refresh_connections(id){
        return api.get('connections/' + id +'/refresh')
    }
    delete_connections(id){
        return api.delete('connections/' + id +'/')
    }
    update_connections(id, data){
        return api_without_preloader.put('connections/' + id + '/', data)
    }
    get_alias(){
        return api.get('connections/alias/')
    }
}
export default new ViewService();