
import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [message, setMessage] = useState('')

  const [form, setForm] = useState({
    name: '',
    department: '',
    salary: '',
  })

  useEffect(() => {
    const controller = new AbortController()

    async function loadEmployees() {
      try {
        const response = await fetch('/api/employees', {
          signal: controller.signal,
        })

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`)
        }

        setEmployees(await response.json())
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message)
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false)
        }
      }
    }

    loadEmployees()
    return () => controller.abort()
  }, [])

  function handleChange(event) {
    const { name, value } = event.target
    setForm((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

function handleEdit(employee)

{
  setEditingId(employee.id)

  setForm({
    name: employee.name,
    department: employee.department,
    salary: String(employee.salary),
  })

  setError('')
  setMessage('')
  window.scrollTo({ top: 0, behavior: 'smooth' })
}


async function handleDelete(employee) {
  const confirmed = window.confirm(
    `Are you sure you want to delete ${employee.name} (ID: ${employee.id})?`
  )

  if (!confirmed) return

  setError('')
  setMessage('')

  try {
    const response = await fetch(`/api/employees/${employee.id}`, {
      method: 'DELETE',
    })

    if (!response.ok) {
      throw new Error(`Failed to delete employee: ${response.status}`)
    }

    setEmployees((previous) =>
      previous.filter((item) => item.id !== employee.id)
    )

    if (editingId === employee.id) {
      setEditingId(null)
      setForm({ name: '', department: '', salary: '' })
    }

    setMessage(`${employee.name} deleted successfully!`)
  } catch (err) {
    setError(err.message)
  }
}



async function handleSubmit(event) {
  event.preventDefault()

  if (saving) return

  setSaving(true)
  setError('')
  setMessage('')

  const isEditing = editingId !== null

  try {
    const url = isEditing
      ? `/api/employees/${editingId}`
      : '/api/employees'

    const method = isEditing ? 'PUT' : 'POST'

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: form.name.trim(),
        department: form.department.trim(),
        salary: Number(form.salary),
      }),
    })

    if (!response.ok) {
      throw new Error(
        `Failed to ${isEditing ? 'update' : 'create'} employee: ${response.status}`
      )
    }

    const savedEmployee = await response.json()

    if (isEditing) {
      setEmployees((previous) =>
        previous.map((employee) =>
          employee.id === editingId
            ? savedEmployee
            : employee
        )
      )
      setMessage('Employee updated successfully!')
    } else {
      setEmployees((previous) => [...previous, savedEmployee])
      setMessage('Employee added successfully!')
    }

    setEditingId(null)
    setForm({
      name: '',
      department: '',
      salary: '',
    })
  } catch (err) {
    setError(err.message)
  } finally {
    setSaving(false)
  }
}


  return (
    <div className="dashboard">
      <h1>Employee Management Dashboard</h1>
      <p>DevOps Three-Tier Application</p>

      <h2>{editingId !== null ? 'Edit Employee' : 'Add Employee'}</h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            id="name"
            name="name"
            value={form.name}
            onChange={handleChange}
            minLength={2}
            maxLength={100}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="department">Department</label>
          <input
            id="department"
            name="department"
            value={form.department}
            onChange={handleChange}
            minLength={2}
            maxLength={50}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="salary">Salary (INR)</label>
          <input
            id="salary"
            name="salary"
            type="number"
            min="1"
            step="1"
            value={form.salary}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={saving}>
          {saving ? 'Saving...' : editingId !== null ? 'Update Employee' : 'Add Employee'}
        </button>
      </form>

      {message && <p role="status">{message}</p>}
      {error && <p role="alert">Error: {error}</p>}

      <h2>Employee List</h2>

      {loading && <p>Loading employees...</p>}

      {!loading && !error && (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Department</th>
              <th>Salary (INR)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((employee) => (
              <tr key={employee.id}>
                <td>{employee.id}</td>
                <td>{employee.name}</td>
                <td>{employee.department}</td>
                <td>{employee.salary.toLocaleString('en-IN')}</td>

<td>
  <button
    type="button"
    onClick={() => handleEdit(employee)}
  >
    Edit
  </button>

<button
  type="button"
  className="delete-button"
  onClick={() => handleDelete(employee)}
>
  Delete
</button>

</td>

              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!loading && !error && employees.length === 0 && (
        <p>No employees found.</p>
      )}
    </div>
  )
}

export default App
