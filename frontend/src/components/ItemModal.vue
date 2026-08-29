<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
    <div class="bg-bomberos-surface border border-bomberos-border rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl animate-in fade-in zoom-in-95 duration-150">
      <!-- Header -->
      <div class="p-5 border-b border-bomberos-border bg-bomberos-card flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          <h3 class="font-bold text-base text-gray-100">Registrar Nuevo Bien en Inventario</h3>
        </div>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white text-base font-bold p-1">
          ✕
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
        <!-- Error Message -->
        <div v-if="errorMsg" class="p-3 rounded-xl bg-red-950/80 border border-red-800 text-red-200 text-xs">
          {{ errorMsg }}
        </div>

        <!-- Nombre -->
        <div>
          <label class="block text-xs font-bold text-gray-300 uppercase tracking-wider mb-1.5">
            Nombre del Bien *
          </label>
          <input
            v-model="form.nombre"
            type="text"
            required
            placeholder="Ej. Manguera 70mm o Motosierra Stihl"
            class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-4 py-2.5 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-bomberos-red"
          />
        </div>

        <!-- Descripción -->
        <div>
          <label class="block text-xs font-bold text-gray-300 uppercase tracking-wider mb-1.5">
            Descripción / Especificación
          </label>
          <textarea
            v-model="form.descripcion"
            rows="2"
            placeholder="Color institucional naranja, medidas o detalles de procedencia..."
            class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-4 py-2 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-bomberos-red"
          ></textarea>
        </div>

        <!-- Categoría & Tipo Dual -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-bold text-gray-300 uppercase tracking-wider mb-1.5">
              Categoría *
            </label>
            <select
              v-model.number="form.id_categoria"
              required
              class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2.5 text-sm text-gray-100 focus:outline-none focus:border-bomberos-red"
            >
              <option v-for="cat in catalogoStore.categorias" :key="cat.id_categoria" :value="cat.id_categoria">
                {{ cat.nombre }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-300 uppercase tracking-wider mb-1.5">
              Clasificación MER v3 *
            </label>
            <select
              v-model.number="form.id_tipo_item"
              required
              class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2.5 text-sm text-gray-100 focus:outline-none focus:border-bomberos-red"
            >
              <option :value="1">Agrupable (Lote / Conteo)</option>
              <option :value="2">Unitario (Etiqueta QR)</option>
            </select>
          </div>
        </div>

        <!-- QR Input (Solo si es Unitario) -->
        <div v-if="form.id_tipo_item === 2" class="p-3.5 rounded-xl bg-red-950/20 border border-red-900/40">
          <label class="block text-xs font-bold text-red-300 uppercase tracking-wider mb-1.5">
            Código QR de Etiqueta *
          </label>
          <div class="flex gap-2">
            <input
              v-model="form.codigo_qr"
              type="text"
              required
              placeholder="Ej. QR-HERR-005"
              class="flex-1 bg-bomberos-card border border-bomberos-border rounded-xl px-4 py-2 text-sm text-gray-100 font-mono focus:outline-none focus:border-bomberos-red"
            />
            <button
              type="button"
              @click="generateQR"
              class="px-3 py-2 bg-bomberos-surface hover:bg-bomberos-border rounded-xl text-xs font-bold text-gray-200 border border-bomberos-border"
            >
              Generar
            </button>
          </div>
          <p class="text-[11px] text-gray-400 mt-1">Este código identifica exclusivamente a este activo físico.</p>
        </div>

        <!-- Cantidad & Estado -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-bold text-gray-300 uppercase tracking-wider mb-1.5">
              Cantidad Inicial *
            </label>
            <input
              v-model.number="form.cantidad"
              type="number"
              min="0"
              :disabled="form.id_tipo_item === 2"
              class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-4 py-2.5 text-sm text-gray-100 disabled:opacity-50 focus:outline-none focus:border-bomberos-red"
            />
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-300 uppercase tracking-wider mb-1.5">
              Estado Físico *
            </label>
            <select
              v-model="form.estado"
              class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2.5 text-sm text-gray-100 focus:outline-none focus:border-bomberos-red"
            >
              <option value="OPERATIVO">OPERATIVO</option>
              <option value="BUENO">BUENO</option>
              <option value="EN_MANTENCION">EN MANTENCIÓN</option>
              <option value="DANADO">DAÑADO</option>
            </select>
          </div>
        </div>

        <!-- Actions -->
        <div class="pt-4 border-t border-bomberos-border flex items-center justify-end gap-3">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2.5 rounded-xl border border-bomberos-border text-sm font-semibold text-gray-300 hover:bg-bomberos-card"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="px-5 py-2.5 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-sm font-bold shadow-lg shadow-red-950/40 transition-all disabled:opacity-50 uppercase tracking-wide"
          >
            {{ loading ? 'Guardando...' : 'Registrar Ítem' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { useCatalogoStore } from '../stores/catalogo'

const emit = defineEmits(['close', 'created'])
const catalogoStore = useCatalogoStore()
const loading = ref(false)
const errorMsg = ref(null)

const form = reactive({
  nombre: '',
  descripcion: '',
  codigo_qr: '',
  id_categoria: 2,
  id_tipo_item: 1,
  cantidad: 1,
  estado: 'OPERATIVO',
})

watch(() => form.id_tipo_item, (newVal) => {
  if (newVal === 2) {
    form.cantidad = 1
    if (!form.codigo_qr) {
      generateQR()
    }
  } else {
    form.codigo_qr = null
  }
})

const generateQR = () => {
  const rand = Math.floor(1000 + Math.random() * 9000)
  form.codigo_qr = `QR-BOM-${rand}`
}

const handleSubmit = async () => {
  loading.value = true
  errorMsg.value = null

  const payload = {
    nombre: form.nombre,
    descripcion: form.descripcion || null,
    codigo_qr: form.id_tipo_item === 2 ? form.codigo_qr : null,
    id_categoria: form.id_categoria,
    id_tipo_item: form.id_tipo_item,
    cantidad: form.cantidad,
    estado: form.estado,
    fecha_vencimiento: null,
  }

  const result = await catalogoStore.createItem(payload)
  loading.value = false

  if (result.success) {
    emit('created')
    emit('close')
  } else {
    errorMsg.value = result.error
  }
}
</script>
