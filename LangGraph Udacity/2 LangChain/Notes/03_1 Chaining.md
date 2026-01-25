# LangChain Concepts in This Notebook - Summary

This notebook demonstrates **LCEL (LangChain Expression Language)** and the **Runnable** interface, which are the foundation for building LangChain pipelines.

## 1. **Basic Chaining (Manual)**

Traditional nested invocation approach:

````python
response = parser.invoke(
    llm.invoke(
        prompt.invoke({"topic": "Python"})
    )
)
````

This is verbose and hard to read when chains get complex.

---

## 2. **Runnables Interface**

All LangChain components implement the `Runnable` interface with three key capabilities:

### **Execute Methods**
- **`invoke()`** - Process single input
- **`batch()`** - Process multiple inputs in parallel
- **`stream()`** - Stream output token-by-token

````python
chain.invoke({"topic": "Python"})
chain.batch([{"topic": "Python"}, {"topic": "Data"}])
for chunk in chain.stream({"topic": "Python"}):
    print(chunk, end="")
````

### **Inspect Methods**
- **`get_input_schema()`** - Expected input structure
- **`get_output_schema()`** - Expected output structure
- **`config_schema()`** - Configuration options

### **Configuration**
Pass metadata, tags, and run names for tracking:

````python
llm.invoke("Hello", config={
    'run_name': 'demo_run',
    'tags': ['demo', 'lcel'],
    'metadata': {'lesson': 2}
})
````

---

## 3. **Composing Chains**

### **RunnableSequence** (Sequential execution)
````python
chain = RunnableSequence(prompt, llm, parser)
chain.invoke({"topic": "Python"})
````

### **RunnableLambda** (Turn functions into Runnables)
````python
my_runnable = RunnableLambda(lambda x: x * 2)
my_runnable.invoke(5)  # Returns 10
````

### **RunnableParallel** (Parallel execution)
````python
parallel_chain = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    triple=RunnableLambda(lambda x: x * 3)
)
parallel_chain.invoke(3)  # {'double': 6, 'triple': 9}
````

---

## 4. **LCEL Pipe Syntax (`|`)**

The **magic** of LCEL - use pipe operator for cleaner composition:

````python
# Instead of this:
chain = RunnableSequence(prompt, llm, parser)

# Write this:
chain = prompt | llm | parser
````

Both are equivalent, but pipe syntax is:
- ✓ More readable
- ✓ More Pythonic
- ✓ Easier to modify
- ✓ Industry standard

---

## 5. **Visualization**

Inspect chain structure with ASCII graph:

````python
chain.get_graph().print_ascii()
````

Shows the flow: `PromptTemplate → ChatOpenAI → StrOutputParser`

---

## Key Takeaways

| Concept | Purpose | Example |
|---------|---------|---------|
| **Runnable** | Base interface for all components | `prompt.invoke()`, `llm.batch()` |
| **RunnableSequence** | Chain components sequentially | `RunnableSequence(a, b, c)` |
| **RunnableParallel** | Execute multiple paths in parallel | `RunnableParallel(x=a, y=b)` |
| **RunnableLambda** | Convert functions to Runnables | `RunnableLambda(my_func)` |
| **LCEL (`\|`)** | Pipe syntax for composition | `prompt \| llm \| parser` |
| **Config** | Add metadata/tracking | `invoke(..., config={...})` |

---

## Why This Matters

LCEL provides:
1. **Streaming support** - Token-by-token output
2. **Batch processing** - Handle multiple requests efficiently
3. **Async support** - Non-blocking execution
4. **Parallel execution** - Run independent tasks simultaneously
5. **Observability** - Built-in tracing and logging
6. **Type safety** - Input/output schema validation

The pipe syntax (`|`) is now the **standard way** to build LangChain applications!