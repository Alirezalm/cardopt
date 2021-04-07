const Problem = {
    template: '#problem-form',
        delimiters: ['[[', ']]'],
    data(){
        return {
            problemData: {},
            optimizing: false
        }
    },
        mounted() {
            this.problemData['name'] = 'distributed sparse logistic regression'
            this.problemData['nVars'] = 10
            this.problemData['nSamples'] = 1000
            this.problemData['nZeros'] = 5
            this.problemData['nNodes'] = 4
            this.problemData['compareTo'] = 'shot'
        },
    methods: {


        onOptimize(){
            // this.optimizing = true
            const url = '/cardopt/dashboard'
            axios.post(url, JSON.stringify(this.problemData)).then(res => {
                console.log(JSON.stringify(this.problemData))
                // this.optimizing = false
                console.log(res.data)

            })
        }
    }
}

const routes = [
    {path: '/problem', component: Problem}
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes: routes
})
const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            url: ''
        }
    },
    methods: {
        onSignOut() {
            this.url = 'http://127.0.0.1:8000/logout'
            axios.get(this.url).then((res) => {
                console.log(res.data)

            })
        }
    }
})

app.use(router)
app.mount('#app')
