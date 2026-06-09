export class OfflineStorage {
  private dbName = 'HabitTrackerDB'
  private version = 1
  private db: IDBDatabase | null = null

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version)
      
      request.onerror = () => reject(request.error)
      request.onsuccess = () => {
        this.db = request.result
        resolve()
      }
      
      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result
        
        if (!db.objectStoreNames.contains('habits')) {
          db.createObjectStore('habits', { keyPath: 'id' })
        }
        if (!db.objectStoreNames.contains('completions')) {
          db.createObjectStore('completions', { keyPath: 'id' })
        }
        if (!db.objectStoreNames.contains('syncQueue')) {
          db.createObjectStore('syncQueue', { keyPath: 'id', autoIncrement: true })
        }
      }
    })
  }

  async saveHabits(habits: any[]): Promise<void> {
    if (!this.db) return
    
    const transaction = this.db.transaction(['habits'], 'readwrite')
    const store = transaction.objectStore('habits')
    
    await store.clear()
    for (const habit of habits) {
      store.add(habit)
    }
    
    return new Promise((resolve, reject) => {
      transaction.oncomplete = () => resolve()
      transaction.onerror = () => reject(transaction.error)
    })
  }

  async getHabits(): Promise<any[]> {
    if (!this.db) return []
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['habits'], 'readonly')
      const store = transaction.objectStore('habits')
      const request = store.getAll()
      
      request.onsuccess = () => resolve(request.result)
      request.onerror = () => reject(request.error)
    })
  }

  async saveCompletions(completions: any[]): Promise<void> {
    if (!this.db) return
    
    const transaction = this.db.transaction(['completions'], 'readwrite')
    const store = transaction.objectStore('completions')
    
    for (const completion of completions) {
      store.put(completion)
    }
    
    return new Promise((resolve, reject) => {
      transaction.oncomplete = () => resolve()
      transaction.onerror = () => reject(transaction.error)
    })
  }

  async getCompletions(): Promise<any[]> {
    if (!this.db) return []
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['completions'], 'readonly')
      const store = transaction.objectStore('completions')
      const request = store.getAll()
      
      request.onsuccess = () => resolve(request.result)
      request.onerror = () => reject(request.error)
    })
  }

  async addToSyncQueue(action: string, data: any): Promise<void> {
    if (!this.db) return
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['syncQueue'], 'readwrite')
      const store = transaction.objectStore('syncQueue')
      const request = store.add({ action, data, timestamp: Date.now() })
      
      request.onsuccess = () => resolve()
      request.onerror = () => reject(request.error)
    })
  }

  async getSyncQueue(): Promise<any[]> {
    if (!this.db) return []
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['syncQueue'], 'readonly')
      const store = transaction.objectStore('syncQueue')
      const request = store.getAll()
      
      request.onsuccess = () => resolve(request.result)
      request.onerror = () => reject(request.error)
    })
  }

  async clearSyncQueue(): Promise<void> {
    if (!this.db) return
    
    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['syncQueue'], 'readwrite')
      const store = transaction.objectStore('syncQueue')
      const request = store.clear()
      
      request.onsuccess = () => resolve()
      request.onerror = () => reject(request.error)
    })
  }
}

export const offlineStorage = new OfflineStorage()
