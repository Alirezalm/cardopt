const SignIn = {

    // delimiters: ['[[', ']]'],
    template: '#login',
    data() {
        return {
            loginInfo: {},
            url: '',
            loggedIn: false

        }
    },
    methods: {


        loginSubmit() {
            this.url = '/cardopt/login'
            axios.post(this.url, JSON.stringify(this.loginInfo)).then(res => {
                if (res.data.status) {
                    this.loggedIn = true
                } else {
                    this.loggedIn = false
                    alert('wrong user name or password')
                }
                console.log('emmited')
                this.$emit('login-event', this.loggedIn)
            })
        }
    }
}



const routes = [
    {path: '/login', component: SignIn},

]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes: routes
})

const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            loginClicked: false,
            loginStatus: false
        }
    },
    mounted() {

        this.isLogin()
    },
    methods: {
        onLogin() {
            this.loginClicked = true

        },
        onHome() {
            this.loginClicked = false
        },
        onLogout() {
            this.url = '/cardopt/logout'
            axios.get(this.url).then((res) => {
                if (res.data.status) {
                    this.loginStatus = false
                    this.loginClicked = false
                }
            })
        },
        loginEvent(status){
           this.loginStatus = status
        },
        isLogin() {
            this.url = '/cardopt/islogin'
            axios.get(this.url).then(res => {

                if (res.data.status) {
                    this.loginStatus = true
                } else {
                    this.loginStatus = false
                }
            })
        },
    }
})
app.use(router)

app.mount('#app')
