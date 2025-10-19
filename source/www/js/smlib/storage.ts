/**
 * Asynchronously stores data in the browser's localStorage.
 * This data will persist between page loads.
 *
 * @param key - The key under which the data should be stored.
 * @param value - The value to be stored.
 */
const save_local = async <T> (key: string, value: T): Promise<void> => {
    try {
        const json = JSON.stringify(value)
        localStorage.setItem(key, json)
    } catch (error) {
        console.error(`Error storing data with key "${key}":`, error)
        throw error
    }
}



/**
 * Asynchronously retrieves data from the browser's localStorage.
 *
 * @param key - The key of the data to retrieve.
 * @returns A promise resolving to the retrieved data, or null if the key doesn't exist.
 */
 const load_local = async <T> (key: string): Promise<T | null> => {
    try {
        const json = localStorage.getItem(key)
        if (json === null) {
            return null
        }
        return JSON.parse(json) as T
    } catch (error) {
        console.error(`Error retrieving data with key "${key}":`, error)
        return null
    }
}



/**
 * Asynchronously stores data in the server's memory.
 * This data is shared between all clients, but is not saved in the database.
 *
 * @param key - The key under which the data should be stored.
 * @param value - The value to be stored.
 */
const save_central = async <T> (key: string, value: T): Promise<void> => {
}



/**
 * Asynchronously retrieves data from the server's memory.
 *
 * @param key - The key of the data to retrieve.
 * @returns A promise resolving to the retrieved data, or null if the key doesn't exist.
 */
const load_central = async <T> (key: string): Promise<T | null> => {
    return null
}



/**
 * Asynchronously stores data in the central database.
 *
 * @param key - The key under which the data should be stored.
 * @param value - The value to be stored.
 */
const save_db = async <T> (key: string, value: T): Promise<void> => {
}



/**
 * Asynchronously retrieves data from the central database.
 *
 * @param key - The key of the data to retrieve.
 * @returns A promise resolving to the retrieved data, or null if the key doesn't exist.
 */
const load_db = async <T> (key: string): Promise<T | null> => {
    return null
}



/******************************************************************************
/
/   Module exports
/
/*****************************************************************************/

export const storage = {
    save_local: save_local,
    load_local: load_local,

    save_central: save_central,
    load_central: load_central,

    save_db: save_db,
    load_db: load_db,
}
