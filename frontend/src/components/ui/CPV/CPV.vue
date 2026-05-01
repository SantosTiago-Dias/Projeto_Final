<script setup lang="ts">
import { Separator } from "@/components/ui/separator";

// Matches your JSON structure: { "codigo": "...", "cpv_descricao": "..." }
interface CPV {
  id_cpv: number;
  codigo: string;
  cpv_descricao: string;
  descricao?: string;
}

interface Props {
  cpvs?: CPV[];
}

defineProps<Props>();
</script>

<template>
  <div v-if="cpvs && cpvs.length" class="space-y-3">
    <div v-for="(item, index) in cpvs" :key="item.id_cpv || index" class="w-full">
      <div class="flex flex-col gap-0.5">
        <!-- CPV Code -->
        <div class="text-xs font-mono font-bold text-foreground">
          {{ item.codigo }}
        </div>

        <!-- CPV Main Description -->
        <div class="text-xs text-muted-foreground leading-tight">
          {{ item.cpv_descricao }}
        </div>


        <div v-if="item.descricao" class="leading-snug mt-1">
          {{ item.descricao }}
        </div>
      </div>

      <!-- Separator -->
      <Separator
          v-if="index !== cpvs.length - 1"
          class="mt-3"
      />
    </div>
  </div>

  <div v-else class="text-xs text-muted-foreground italic">
    Nenhum CPV registado.
  </div>
</template>