import { React, useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { Form, Button, Row, Col, Card, InputGroup } from 'react-bootstrap';
import { TagsInput } from "react-tag-input-component";

const SearchForm = ({ onSearch, initialData }) => {
  const {
    control,
    handleSubmit,
    reset,
    watch,
    formState: { errors }
  } = useForm({
    defaultValues: {
      target_roles: [],
      desired_locations: [],
      skills: [],
      salary_min: 0,
      salary_max: 200000
    }
  });

  useEffect(() => {
    if (initialData) {
      reset(initialData);
    }
  }, [initialData, reset]);

  const salaryMin = watch("salary_min");

  const onSubmit = (data) => {
    const formattedData = {
      ...data,
      salary_min: parseInt(data.salary_min),
      salary_max: parseInt(data.salary_max)
    };
    onSearch(formattedData);
  };

  return (
    <Card className="shadow-sm border-0 mb-4">
      <Card.Body className="p-4">
        <h4 className="mb-4 fw-bold">Job Search Preferences</h4>
        <Form onSubmit={handleSubmit(onSubmit)}>

          {/* Tag Input for Roles */}
          <Form.Group className="mb-3">
            <Form.Label className="small fw-bold text-muted">Target Job Titles</Form.Label>
            <Controller
              name="target_roles"
              control={control}
              rules={{ required: "At least one role is required" }}
              render={({ field }) => (
                <TagsInput
                  value={field.value}
                  onChange={field.onChange}
                  name="roles"
                  placeHolder="Press Enter to add roles (e.g. Software Engineer)"
                />
              )}
            />
            {errors.target_roles && <div className="text-danger small mt-1">{errors.target_roles.message}</div>}
          </Form.Group>

          <Row>
            {/* Tag Input for Locations */}
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="small fw-bold text-muted">Preferred Locations</Form.Label>
                <Controller
                  name="desired_locations"
                  control={control}
                  render={({ field }) => (
                    <TagsInput
                      value={field.value}
                      onChange={field.onChange}
                      placeHolder="e.g. Seattle, Remote"
                    />
                  )}
                />
              </Form.Group>
            </Col>

            {/* Tag Input for Skills */}
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="small fw-bold text-muted">Key Skills</Form.Label>
                <Controller
                  name="skills"
                  control={control}
                  render={({ field }) => (
                    <TagsInput
                      value={field.value}
                      onChange={field.onChange}
                      placeHolder="e.g. Python, React"
                    />
                  )}
                />
              </Form.Group>
            </Col>
          </Row>

          {/* Salary inputs remain the same as standard inputs */}
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="small fw-bold text-muted">Min Salary</Form.Label>
                <InputGroup>
                  <InputGroup.Text>$</InputGroup.Text>
                  <Form.Control type="number" {...control.register("salary_min")} />
                </InputGroup>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label className="small fw-bold text-muted">Max Salary</Form.Label>
                <InputGroup>
                  <InputGroup.Text>$</InputGroup.Text>
                  <Form.Control
                    type="number"
                    {...control.register("salary_max", {
                      validate: v => parseInt(v) >= parseInt(salaryMin) || "Must be ≥ Min"
                    })}
                    isInvalid={!!errors.salary_max}
                  />
                </InputGroup>
              </Form.Group>
            </Col>
          </Row>

          <div className="d-grid mt-3">
            <Button variant="primary" type="submit" className="py-2 fw-bold">
              Search
            </Button>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default SearchForm;