<template>
  <div class="container">
    <p v-if="loading">A carregar...</p>

    <div v-if="contract">
      <h1>{{ contract.contrato.objeto }}</h1>

      <h2>Detalhes do Contrato</h2>
      <table class="contracts-table">
        <tbody>
          <tr><td>Descrição</td><td>{{ contract.contrato.descricao }}</td></tr>
          <tr><td>Data Publicação</td><td>{{ contract.contrato.data_publicacao }}</td></tr>
          <tr><td>Data Celebração</td><td>{{ contract.data.data_extenso }}</td></tr>
          <tr><td>Valor Contratual</td><td>{{ formatCurrency(contract.contrato.valor_contratual) }}</td></tr>
          <tr><td>Prazo Execução</td><td>{{ contract.contrato.prazo_execucao }} dias</td></tr>
          <tr><td>Local Execução</td><td>{{ contract.contrato.local_execucao }}</td></tr>
          <tr><td>Regime</td><td>{{ contract.contrato.regime }}</td></tr>
          <tr><td>Tipo Contrato</td><td>{{ contract.tipo_contrato.tipo }}</td></tr>
          <tr><td>Procedimento</td><td>{{ contract.tipo_procedimento.tipo }}</td></tr>
          <tr><td>Observações</td><td>{{ contract.contrato.observacoes }}</td></tr>
        </tbody>
      </table>

      <h2>Entidade Adjudicante</h2>
      <table class="contracts-table">
        <tbody>
          <tr><td>Nome</td><td>{{ contract.adjudicanteRel.nome }}</td></tr>
          <tr><td>NIF</td><td>{{ contract.adjudicanteRel.nif }}</td></tr>
          <tr><td>Localização</td><td>{{ contract.adjudicanteRel.pais }}</td></tr>
          <tr><td>Total Adjudicado</td><td>{{ formatCurrency(contract.adjudicanteRel.total_adjudicante) }}</td></tr>
          <tr><td>Nº Contratos</td><td>{{ contract.adjudicanteRel.num_contratos_adjudicante }}</td></tr>
        </tbody>
      </table>

      <h2>Entidades Concorrentes</h2>
      <table class="contracts-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>NIF</th>
            <th>Nº Contratos</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(ent, i) in contract.entidades" :key="i">
            <td>{{ ent.nome }}</td>
            <td>{{ ent.nif }}</td>
            <td>{{ ent.num_contratos_adjudicatario }}</td>
          </tr>
        </tbody>
      </table>

    </div>

    <p v-if="!loading && !contract">Contrato não encontrado</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      contract: null,
      loading: true
    }
  },
  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat('pt-PT', {
        style: 'currency',
        currency: 'EUR'
      }).format(Number(value))
    }
  },
  mounted() {
    const id = this.$route.params.id

    fetch(`http://localhost:8000/api/contracts/${id}`)
      .then(res => res.json())
      .then(data => {
        this.contract = data
        this.loading = false
      })
      .catch(err => {
        console.error(err)
        this.loading = false
      })
  }
}
</script>
