const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data(){
        return {
            url : ''
        }
    },
    methods: {
        onSignOut(){
            this.url = 'http://127.0.0.1:8000/logout'
            axios.get(this.url).then((res) => {
                console.log(res.data)

            })
        }
    }
})


app.mount('#app')
