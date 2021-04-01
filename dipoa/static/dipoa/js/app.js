const SignIn = {

    // delimiters: ['[[', ']]'],
    template: '#login',
    methods: {

    }
}

const Salam = {

    // delimiters: ['[[', ']]'],
    template: '#salamworld'
}

const routes = [
    {path: '/login', component: SignIn},
    {path: '/salam', component: Salam}
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes: routes
})

const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            loginClicked: false
        }
    },
    methods: {
        onLogin(){
            this.loginClicked = true

        },
        onHome(){
            this.loginClicked = false
        }
    }
})
app.use(router)

app.mount('#app')
