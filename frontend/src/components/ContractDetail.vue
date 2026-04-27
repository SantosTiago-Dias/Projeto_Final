<script setup>
import { onMounted, ref } from 'vue'

import {
    Table,
    TableBody,
    TableCell,
    TableRow,
    TableHeader,
    TableHead
} from "@/components/ui/table"

const contract = ref(null)
const loading = ref(true)

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-PT', {
        style: 'currency',
        currency: 'EUR'
    }).format(Number(value))
}

function formatBool(value) {
    return value === 1 || value === true ? 'Sim' : 'Não'
}

function formatNull(value) {
    return value ?? 'Não aplicável'
}

onMounted(async () => {
    const id = window.location.pathname.split('/').pop()

    try {
        const res = await fetch(`http://localhost:8000/api/contracts/${id}`)
        contract.value = await res.json()
    } catch (err) {
        console.error(err)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="container space-y-8">

        <p v-if="loading">A carregar...</p>

        <div v-if="contract" class="space-y-10">

            <h1 class="text-2xl font-bold">
                {{ contract.contrato.objeto }}
            </h1>

            <!-- detalhes contrato -->
            <section>
                <h2 class="text-lg font-semibold mb-2">Contrato</h2>

                <Table class="w-full table-fixed text-sm">
                    <TableBody>

                        <TableRow>
                            <TableCell class="font-medium">Descrição</TableCell>
                            <TableCell class="whitespace-normal break-words leading-relaxed">{{
                                contract.contrato.descricao }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Data Publicação</TableCell>
                            <TableCell>{{ contract.contrato.data_publicacao }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Data Celebração</TableCell>
                            <TableCell>{{ contract.contrato.data_celebracao }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Data Fecho</TableCell>
                            <TableCell>{{ formatNull(contract.contrato.data_fecho_contrato) }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Valor Contratual</TableCell>
                            <TableCell class="text-green-600 font-semibold">
                                {{ formatCurrency(contract.contrato.valor_contratual) }}
                            </TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Valor Total Efetivo</TableCell>
                            <TableCell class="text-green-600 font-semibold">
                                {{ formatNull(contract.contrato.valor_total_efetivo) }}
                            </TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Prazo Execução</TableCell>
                            <TableCell>{{ contract.contrato.prazo_execucao }} dias</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Local Execução</TableCell>
                            <TableCell class="truncate">{{ contract.contrato.local_execucao }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Regime</TableCell>
                            <TableCell class="truncate">{{ contract.contrato.regime }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Tipo Fim Contrato</TableCell>
                            <TableCell>{{ contract.contrato.tipo_fim_contrato }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Critérios Materiais</TableCell>
                            <TableCell>{{ formatBool(contract.contrato.crit_materiais) }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Contrato Ecológico</TableCell>
                            <TableCell>{{ formatBool(contract.contrato.contrato_ecologico) }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Procedimento Centralizado</TableCell>
                            <TableCell>{{ formatBool(contract.contrato.procedimento_centralizado) }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Acordos Quadro</TableCell>
                            <TableCell>{{ contract.contrato.num_acordos_quadro }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Descrição Acordo Quadro</TableCell>
                            <TableCell class="truncate">{{ contract.contrato.desc_acordo_quadro }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Link Peças</TableCell>
                            <TableCell class="truncate">{{ contract.contrato.link_pecas }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Observações</TableCell>
                            <TableCell class="truncate">{{ contract.contrato.observacoes }}</TableCell>
                        </TableRow>

                        <TableRow>
                            <TableCell class="font-medium">Fundamentação Ajuste Direto</TableCell>
                            <TableCell class="truncate">
                                {{ contract.contrato.fundamentacao_ajuste_directo }}
                            </TableCell>
                        </TableRow>

                    </TableBody>
                </Table>
            </section>

            <!-- adjudicante -->
            <section>
                <h2 class="text-lg font-semibold mb-2">Entidade Adjudicante</h2>

                <Table class="w-full table-fixed text-sm">
                   <TableHeader class="bg-gray-50">
                        <TableRow>
                            <TableHead class="w-[50%]">Nome</TableHead>
                            <TableHead class="w-[25%] text-center">NIF</TableHead>
                            <TableHead class="w-[25%] text-center">Contratos</TableHead>
                        </TableRow>
                    </TableHeader>

                    <TableBody>
                        <TableRow class="hover:bg-gray-50 transition-colors">
                            <TableCell class="truncate">{{ contract.adjudicanteRel.nome }}</TableCell>
                            <TableCell class="text-center">{{ contract.adjudicanteRel.nif }}</TableCell>
                            <TableCell class="text-center">
                                {{ contract.adjudicanteRel.num_contratos_adjudicante }}
                            </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </section>

            <!-- adjudicatario -->
            <section>
                <h2 class="text-lg font-semibold mb-2">Entidade Adjudicatária</h2>

                <Table class="w-full table-fixed text-sm">
                    <TableHeader class="bg-gray-50">
                        <TableRow>
                            <TableHead class="w-[50%]">Nome</TableHead>
                            <TableHead class="w-[25%] text-center">NIF</TableHead>
                            <TableHead class="w-[25%] text-center">Contratos</TableHead>
                        </TableRow>
                    </TableHeader>

                    <TableBody>
                        <TableRow class="hover:bg-gray-50 transition-colors">
                            <TableCell class="truncate">{{ contract.adjudicatario.nome }}</TableCell>
                            <TableCell class="text-center">{{ contract.adjudicatario.nif }}</TableCell>
                            <TableCell class="text-center">
                                {{ contract.adjudicatario.num_contratos_adjudicatario }}
                            </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </section>

            <!-- entidades concorrentes -->
            <section v-if="contract.entidades && contract.entidades.length > 0">
                <h2 class="text-lg font-semibold mb-2">Entidades Concorrentes</h2>

                <Table class="w-full table-fixed text-sm">

                    <TableHeader class="bg-gray-50">
                        <TableRow>
                            <TableHead class="w-[50%]">Nome</TableHead>
                            <TableHead class="w-[25%] text-center">NIF</TableHead>
                            <TableHead class="w-[25%] text-center">Contratos</TableHead>
                        </TableRow>
                    </TableHeader>

                    <TableBody>
                        <TableRow v-for="(ent, i) in contract.entidades" :key="i"
                            class="hover:bg-gray-50 transition-colors">
                            <TableCell class="truncate">{{ ent.nome }}</TableCell>
                            <TableCell class="text-center">{{ ent.nif }}</TableCell>
                            <TableCell class="text-center">
                                {{ ent.num_contratos_adjudicatario }}
                            </TableCell>
                        </TableRow>
                    </TableBody>

                </Table>
            </section>

        </div>

        <p v-if="!loading && !contract">
            Contrato não encontrado
        </p>

    </div>
</template>