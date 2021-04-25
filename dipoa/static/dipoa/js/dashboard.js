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
        this.problemData['name'] = 'dslr'
        this.problemData['nVars'] = 10
        this.problemData['nSamples'] = 100
        this.problemData['nZeros'] = 5
        this.problemData['nNodes'] = 4
        this.problemData['compareTo'] = 'shot'
        this.problemData['soc'] = false
        this.problemData['sfp'] = true
    },
    methods: {

        onSave() {
            console.log('form saved');
            if (this.problemData.sfp) {
                this.problemData.sfp = 1

            } else {
                this.problemData.sfp = 0

            }
            if (this.problemData.soc) {

                this.problemData.soc = 1
            } else {

                this.problemData.soc = 0
            }
            if (this.problemData.name === 'dsqcqp'){
                delete this.problemData.nSamples
            }
            this.$emit('form-saved', this.problemData)

            if (this.problemData.sfp) {
                this.problemData.sfp = true

            } else {
                this.problemData.sfp = false

            }
            if (this.problemData.soc) {

                this.problemData.soc = true
            } else {

                this.problemData.soc = false
            }

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
            isOptimizing: false,
            notify: false,
            history: [],
            dbInteraction: false

        }
    },
    methods: {
        onClear() {
            this.url = '/cardopt/app/dashboard/clear'
            this.dbInteraction = true
            axios.get(this.url).then(res => {
                console.log(res.data)
                this.dbInteraction = false
                this.history = []
            })
        },

        onShowResults() {
            this.url = '/cardopt/app/dashboard/history'
            this.dbInteraction = true
            axios.get(this.url).then(res => {
                console.log(res.data['history'])
                this.history = []
                let id = res.data['history'].length + 1
                for (let item of res.data['history']) {
                    id--
                    item.id = id
                    item.optimal_obj = Number(item.optimal_obj).toFixed(5)
                    item.relative_gap = Number(item.relative_gap).toFixed(5)
                    item.elapsed_time = Number(item.elapsed_time).toFixed(5)
                    item.number_of_samples = Number(item.number_of_samples) * Number(item.number_of_cores)
                    item.soc = item.soc.toLowerCase()
                    item.sfp = item.sfp.toLowerCase()
                    this.history.push(item)
                    console.log(item)
                }
                this.dbInteraction = false
            })
        },

        onOptimize() {
            this.isOptimizing = true
            this.notify = false

            const url = '/cardopt/app/dashboard/opt'
            axios.post(url, JSON.stringify(this.data)).then(res => {
                console.log(JSON.stringify(this.data))
                this.isOptimizing = false
                console.log(res.data)

                this.solutionData = res.data
                this.solutionData.obj = Number(this.solutionData.obj).toFixed(5)
                this.solutionData.elapsed_time = Number(this.solutionData.elapsed_time).toFixed(5)
                this.solutionData.gap = Number(this.solutionData.gap).toFixed(5)
                this.notify = true
                this.plotCharts()

            }).catch(error => {
                this.isOptimizing = false
                this.notify = false
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
                        fill: false,
                        data: this.solutionData['lb'],

                    },
                        {
                            label: 'Upper bound',
                            data: this.solutionData['ub'],
                            borderColor: 'blue',
                            fill: false,
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
