<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  data: Array,
  columns: Array,
  filterKey: String,
  selectedField: String,
})

const sortKey = ref('')
const sortOrders = ref(props.columns.reduce((o, key) => ((o[key] = 1), o), {}))

const getNestedValue = (obj, path) => {
  return path.split('.').reduce((acc, key) => acc?.[key], obj)
}

const filteredData = computed(() => {
  let { data, filterKey, selectedField } = props
  if (filterKey && data) {
    filterKey = filterKey.toLowerCase()
    data = data.filter((row) => {
      const keysToSearch = selectedField === 'all' ? getAllKeys(row) : [selectedField]
      return keysToSearch.some(keyPath => {
        const value = getNestedValue(row, keyPath)
        return String(value).toLocaleLowerCase().includes(filterKey)
      })
    })
  }
  const key = sortKey.value
  if (key && data.length) {
    const order = sortOrders.value[key]
    data = data.slice().sort((a, b) => {
      const valA = getNestedValue(a, key)
      const valB = getNestedValue(b, key)
      return (valA === valB ? 0 : valA > valB ? 1 : -1) * order
    })
  }
  return data
})

// Helper function to get all nested keys from an object
/**
 * Recursively extracts all nested key paths from an object using dot notation
 *
 * @param {Object} obj - The object to traverse and extract keys from
 * @param {string} prefix - The current path prefix (used internally for recursion)
 * @returns {string[]} Array of all nested key paths (e.g., ['name', 'address.city', 'address.location.lat'])
 *
 * Example:
 *   const data = { user: { name: 'John', address: { city: 'NYC' } } }
 *   getAllKeys(data) // Returns: ['user.name', 'user.address', 'user.address.city']
 */

function getAllKeys(obj, prefix = '') {
  // DEBUG: Log function invocation with current parameters
  // console.log('getAllKeys fired',{'obj': obj, 'prefix': prefix})

  // Initialize an array to store all the key paths we find
  let keys = []
  console.log({ keys: keys }) // DEBUG: Initial empty array

  // BASE CASE: If obj is null/undefined or not an object, return empty array
  // This prevents errors and stops recursion when we hit primitive values
  if (!obj || typeof obj !== 'object') {
    return keys
  }

  // console.log({ 'full obj': obj, 'nome autore': obj?.autore?.nome }) // DEBUG: Log the object being processed
  // // Or check all at once with more info
  // console.log('Full path check:', {
  //   hasObj: !!obj,
  //   hasObject: !!obj?.object,
  //   hasAutore: !!obj?.object?.autore,
  //   hasNome: !!obj?.object?.autore?.nome,
  //   value: obj?.object?.autore?.nome,
  // })

  // STEP 1: Loop through every property in the current object
  for (const key in obj) {
    // STEP 2: Build the complete dot-notation path
    // - If we have a prefix (we're nested), combine: prefix.key
    // - If no prefix (we're at root), just use the key
    // Example: prefix='address', key='city' → 'address.city'
    const fullKey = prefix ? `${prefix}.${key}` : key
    // console.log({'fullKey': fullKey}) // DEBUG: Log the full path we're working with

    // STEP 3: Check if this property's value is a nested object
    // Conditions:
    // - Is it an 'object' type? (not string, number, boolean, etc.)
    // - Is it NOT null? (null is technically an object but we want to treat it as a leaf)
    // - Is it NOT an Array? (we treat arrays as leaf values, not nested objects)
    if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
      // STEP 3A: RECURSIVE CASE - Value is a nested object
      // Recursively call getAllKeys on the nested object
      // Pass the fullKey as the new prefix to maintain the dot-notation path
      // Concatenate the returned keys to our current keys array
      // Example: If obj[key] is { city: 'NYC', zip: '10001' }
      // This will return ['city', 'zip'] which becomes ['address.city', 'address.zip']
      keys = keys.concat(getAllKeys(obj[key], fullKey))
    } else {
      // STEP 3B: BASE CASE - Value is a leaf (primitive, null, or array)
      // We've reached the end of this path, so add the full path to our keys array
      // Example: key='name' with no prefix → push('name')
      // Example: key='city' with prefix='address' → push('address.city')
      keys.push(fullKey)
    }
  }

  // STEP 4: Return the complete array of all key paths found
  return keys
}

function sortBy(key) {
  sortKey.value = key
  sortOrders.value[key] *= -1
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<template>
  <table v-if="filteredData.length">
    <thead>
      <tr>
        <th v-for="key in columns" @click="sortBy(key)" :class="{ active: sortKey == key }">
          {{ capitalize(key) }}
          <span class="arrow" :class="sortOrders[key] > 0 ? 'asc' : 'dsc'"> </span>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="entry in filteredData">
        <td v-for="key in columns">
          {{ getNestedValue(entry, key) }}
        </td>
      </tr>
    </tbody>
  </table>
  <p v-else>No matches found.</p>
</template>

<style scoped>
table {
  border: 2px solid #42b983;
  border-radius: 3px;
  background-color: #fff;
}

th {
  background-color: #42b983;
  color: rgba(255, 255, 255, 0.66);
  cursor: pointer;
  user-select: none;
}

td {
  background-color: #f9f9f9;
}

th,
td {
  min-width: 120px;
  padding: 10px 20px;
}

th.active {
  color: #fff;
}

th.active .arrow {
  opacity: 1;
}

.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.asc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid #fff;
}

.arrow.dsc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid #fff;
}
</style>
