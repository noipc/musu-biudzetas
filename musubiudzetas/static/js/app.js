"use strict";

const Regions = {
    props: ['region'],
    template: `
    <div>
        <h2>{{ header }}</h2>
        <ul>
            <li v-for='region in regions' v-bind:key='region.id'>{{region.name}}
                <ul>
                    <li v-for='municipality in region.municipalities' v-bind:key='municipality.id'>
                        <router-link v-bind:to='{ name:"municipality", params:{id: municipality.id} }'>{{municipality.name}}</router-link>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
    `,
    data() {
        return {
            header: 'Savivaldybės',
            regions: []
        }
    },
    created() {
        fetch('/api/regions/')
        .then((res) => {return res.json()})
        .then((data) => {this.regions = data});
    }
};

const Municipality = {
    template: `
    <div>
        <h2>{{ municipality.name }}</h2>
        <span v-if='loading'>Loading...</span>
        <ul v-else>
            <li v-for='entity in municipality.entities' v-bind:key='entity.id'>
                <router-link v-bind:to='{name:"entity", params:{id: entity.id} }'>{{entity.name}}</router-link>
            </li>
        </ul>
    </div>
    `, 
    data() {
        return {
            loading: false,
            municipality: []
        }
    },
    created() {
        this.getData()
    },
    methods: {
        getData() {
            this.loading = true;
            fetch('/api/municipalities/' + this.$route.params.id)
            .then((res) => {return res.json()})
            .then((data) => {
                this.loading = false;
                this.municipality = data
            });
        }
    }
};

const Entity = {
    template:`
        <div>
            <span v-if='loading'>Loading...</span>
            <h2>{{ entity.name }}</h2>
            <table>
                <thead>
                    <th>Lėšų kilmė</th>
                    <th>Metai</th>
                    <th>Suma</th>
                </thead>
                <tbody>
                    <tr v-for='budget in entity.budgets' v-bind:key='budget.id'>
                        <td>{{ budget.b_source}}</td>
                        <td>{{ budget.year}}</td>
                        <td>{{ budget.amount}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    `,
    data() {
        return {
            loading: false,
            entity: []
        }
    },
    created() {
        this.getData()
    },
    methods: {
        getData() {
            this.loading = true;
            fetch('/api/entities/' + this.$route.params.id)
            .then((res) => {return res.json()})
            .then((data) => {
                this.loading = false;
                this.entity = data
            });
        }
    }
}

const routes = [
    { path: '/', component: Regions },
    { path: '/savivaldybes/:id', name:'municipality', component: Municipality, props: true },
    { path: '/imones/:id', name: 'entity', component: Entity, props: true}
  ]


const router = new VueRouter({
    routes
})

const app = new Vue({
    el: "#app",
    router
}).$mount('#app');

