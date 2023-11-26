# YT-GraphQL-Django-Get-Started
 
```shell
query {
  allBooks(title: "react") {
    id
    title
    excerpt
  }
}

query {
  allBooks {
    id
    title
    excerpt
  }
}

# create a book
mutation {
  createBook(title: "The Great Gatsby", excerpt: "This is an excerpt from The Great Gatsby.") {
    book {
      id
      title
      excerpt
    }
  }
}

# delete a book
mutation {
  deleteBook(id: "1") {
    ok
  }
}
# update a book
mutation {
  updateBook(id: "2", title: "Updated Title", excerpt: "Updated excerpt.") {
    book {
      id
      title
      excerpt
    }
  }
}


#query

query {
  order(id: 2) {
    id
    quantity
    customer {
      id
      name
    }
    book {
      id
      title
    }
  }
}

# create an order
mutation {
  createOrder(customerId: 1, bookId: 2, quantity: 3) {
    order {
      id
      customer {
        id
        name 
      }
      book {
        id
        title 
      }
      quantity
    }
  }
}

```