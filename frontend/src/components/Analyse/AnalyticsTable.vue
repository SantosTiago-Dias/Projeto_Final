<template>
  <div>
    <div v-if="loading" class="text-muted-foreground">
      A carregar dados...
    </div>

    <Table v-else class="w-full table-fixed">
      <TableHeader>
        <TableRow>
          <TableHead
              v-for="col in columns"
              :key="col.key"
              :class="col.class"
          >
            {{ col.label }}
          </TableHead>
        </TableRow>
      </TableHeader>

      <TableBody>
        <TableRow
            v-for="item in items"
            :key="item[rowKey]"
            class="hover:bg-muted/50 transition-colors cursor-pointer"
            @click="onRowClick && onRowClick(item)"
        >
          <TableCell
              v-for="col in columns"
              :key="col.key"
              :class="col.cellClass"
          >
            <slot
                :name="col.key"
                :item="item"
            >
              {{ item[col.key] }}
            </slot>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>

<script setup>
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  columns: {
    type: Array,
    required: true,
  },
  rowKey: {
    type: String,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  onRowClick: {
    type: Function,
    default: null,
  },
})
</script>
