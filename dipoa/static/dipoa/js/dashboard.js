const Problem = {
    template: '#problem-form',
    delimiters: ['[[', ']]'],
    data() {
        return {
            problemData: {},
            optimizing: false,
            formSaved: false
        }
    },
    mounted() {
        this.problemData['name'] = 'distributed sparse logistic regression'
        this.problemData['nVars'] = 10
        this.problemData['nSamples'] = 100
        this.problemData['nZeros'] = 5
        this.problemData['nNodes'] = 4
        this.problemData['compareTo'] = 'shot'
    },
    methods: {

        onSave() {
            console.log('form saved');
            this.$emit('form-saved', this.problemData)
        },
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
            url: '',
            formSaved: false,
            data: {},
            solutionData: '',
            isOptimizing : false,

        }
    },
    methods: {
        onShowResults(){
            this.url = '/cardopt/app/dashboard/history'
            axios.get(this.url).then(res=>{
                console.log(res.data)
            })
        },
        onOptimize() {
            this.isOptimizing = true
            const url = '/cardopt/app/dashboard/opt'
            axios.post(url, JSON.stringify(this.data)).then(res => {
                console.log(JSON.stringify(this.data))
                this.isOptimizing = false
                console.log(res.data)

                this.solutionData = res.data

                this.plotCharts()

            }).catch(error =>{
                this.isOptimizing = false
            })
        },
        onFormSaved(problemData) {
            console.log(problemData);
            this.formSaved = true
            this.data = problemData
        },

        onSignOut() {
            this.url = 'http://127.0.0.1:8000/cardopt/logout'
            axios.get(this.url).then((res) => {
                console.log(res.data)

            })
        },
        plotCharts() {
            let ctx = document.getElementById('myChart').getContext('2d')
            var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: this.solutionData['iter'],
        datasets: [{
            label: 'Lower bound',
            borderColor: 'red',
            fill:false,
            data: this.solutionData['lb'],

        },
            {
                label: 'Upper bound',
                data: this.solutionData['ub'],
                borderColor: 'blue',
                 fill:false,
            }
        ]
    },

    // Configuration options go here
    options: {
        elements: {
        line: {
            tension: 0
        }
    }
    }
});
        }
    }
})

app.use(router)
app.mount('#app')
