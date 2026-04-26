<template>
  <div class="container">
    <h1>Contratos</h1>

    <p v-if="loading">A carregar...</p>

    <table v-else class="contracts-table">
      <thead>
        <tr>
          <th>Objeto</th>
          <th>Adjudicante</th>
          <th>Tipo Contrato</th>
          <th>Procedimento</th>
          <th>Data Assinatura</th>
          <th>Valor</th>
          <th>Ações</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in contracts" :key="item.contrato.chave_contratos">
          <td>{{ item.contrato.objeto }}</td>
          <td>{{ item.adjudicanteRel.nome }}</td>
          <td>{{ item.tipo_contrato.tipo }}</td>
          <td>{{ item.tipo_procedimento.tipo }}</td>
          <td>{{ item.data.data_extenso }}</td>
          <td>{{ formatCurrency(item.contrato.valor_contratual) }}</td>
          <td>
            <router-link
              :to="`/contracts/${item.contrato.chave_contratos}`"
              class="btn"
            >
              Detalhes
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import '../style.css'

export default {
  data() {
    return {
      contracts: [],
      loading: true
    }
  },
  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat('pt-PT', {
        style: 'currency',
        currency: 'EUR'
      }).format(value)
    }
  },
  mounted() {
    fetch('http://localhost:8000/api/contracts')
      .then(res => res.json())
      .then(data => {
        this.contracts = data.data
        this.loading = false
      })
      .catch(err => {
        console.error(err)
        this.loading = false
      })
  }
}
</script>